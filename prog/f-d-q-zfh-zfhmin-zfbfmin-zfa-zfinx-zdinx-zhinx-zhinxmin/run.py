#!/usr/bin/env python3
"""Build the identical ELF for both models, run it, compare architectural signatures."""
from pathlib import Path
import argparse, concurrent.futures, hashlib, json, os, re, shutil, struct, subprocess, time
ROOT=Path(__file__).resolve().parent
DEFAULT_SAIL=Path.home()/'projects/testkit4rv/builtin/sail/sail_riscv_sim'
def command(cmd,timeout=120):
 start=time.monotonic()
 try:
  r=subprocess.run([str(x) for x in cmd],capture_output=True,text=True,timeout=timeout)
  return dict(command=[str(x) for x in cmd],returncode=r.returncode,seconds=round(time.monotonic()-start,3),stdout=r.stdout,stderr=r.stderr)
 except subprocess.TimeoutExpired as e:
  return dict(command=[str(x) for x in cmd],returncode=None,seconds=round(time.monotonic()-start,3),stdout=(e.stdout or b'').decode(errors='replace') if isinstance(e.stdout,bytes) else e.stdout or '',stderr='TIMEOUT')
def signature(path):
 return b''.join(bytes.fromhex(s.strip())[::-1] for s in path.read_text().splitlines() if s.strip())
def configure(sail,p):
 raw=subprocess.check_output([str(sail),*(['--rv32'] if p['xlen']==32 else []),'--print-default-config'],text=True)
 d=json.loads(re.sub(r'//[^\n]*','',raw))
 # Keep structural/default parameters but disable unrelated extensions, so enabling
 # vector, compressed or board extensions cannot accidentally supply a missing FP op.
 enabled={'M','A','S','U','Zicsr'}|{x.capitalize() if x in ['f','d','q'] else {'zfh':'Zfh','zfhmin':'Zfhmin','zfa':'Zfa','zfbfmin':'Zfbfmin','zfinx':'Zfinx','zdinx':'Zdinx','zhinx':'Zhinx','zhinxmin':'Zhinxmin'}[x] for x in p['ext']}
 for k,v in d['extensions'].items():
  if 'supported' in v:v['supported']=k in enabled
 d['extensions']['V']['support_level']='Disabled'
 d['extensions']['Stateen']['Smstateen']['supported']=False
 d['extensions']['Stateen']['Ssstateen']['supported']=False
 d['base']['xlen']=p['xlen']
 d['base']['medeleg']['delegatable_bits']['value']='0x0'
 d['base']['mideleg']['delegatable_bits']['value']='0x0'
 if p['xlen']==32:
  d['base']['hpmevent_width_bits']=32
  d['memory']['physaddr_bits']=34;d['memory']['asidlen']=9;d['memory']['vmidlen']=7
  for k in ['Sv39','Sv48','Sv57']:d['extensions'][k]['supported']=False
  d['extensions']['Sv32']['supported']=True
 else:d['extensions']['Sv39']['supported']=True
 if p['bank']=='x':
  d['base']['mstatus']['fs_legal_states']='ExtContext_Off'
  # Sail 0.15 sizes its FP helper type from D.supported only, ignoring Zdinx.
  # Allocate 64-bit helper storage; F remains false and misa.D/F stay zero.
  if 'zdinx' in p['ext']:d['extensions']['D']['supported']=True
 return d

def run_profile(name,p,args):
 out=ROOT/'results'/name;out.mkdir(parents=True,exist_ok=True)
 build=ROOT/'build'/name;build.mkdir(parents=True,exist_ok=True)
 src=ROOT/'generated'/name
 elf=build/'suite.elf'
 cc=[args.cc,f'-march=rv{p["xlen"]}imafd_zicsr','-mabi='+('lp64' if p['xlen']==64 else 'ilp32'),'-nostdlib','-nostartfiles','-Wl,--no-relax','-T',ROOT/'link.ld',src/'suite.S','-o',elf]
 compiled=command(cc,args.timeout);(out/'build.json').write_text(json.dumps(compiled,indent=2)+'\n')
 result={'profile':name,'cases':p['cases'],'build':compiled['returncode']}
 if compiled['returncode']!=0:return dict(result,status='build_failed')
 syms=subprocess.check_output([args.nm,str(elf)],text=True)
 (out/'symbols.txt').write_text(syms)
 targetpcs={int(m[2]):int(m[1],16) for m in re.finditer(r'^([0-9a-f]+) \w target_(\d+)$',syms,re.M)}
 isa=f'rv{p["xlen"]}ima'+''.join(x for x in ['f','d','q'] if x in p['ext'])+'_zicsr'+''.join('_'+x for x in p['ext'] if x not in ['f','d','q'])
 spike=command([args.spike,'--isa='+isa,'-m128','+signature='+str(out/'spike.sig'),'+signature-granularity=4',elf],args.timeout)
 (out/'spike.json').write_text(json.dumps(spike,indent=2)+'\n')
 result['spike_returncode']=spike['returncode']
 if 'q' in p['ext'] and not args.sail_has_q:
  # Q is absent from this Sail build's configuration schema; never call a trap a pass.
  result.update(sail_status='unsupported_Q',status='single_model_only')
 else:
  config=configure(args.sail,p);configpath=ROOT/'configs'/(name+'.json');configpath.write_text(json.dumps(config,indent=2)+'\n')
  (out/'sail.sig').unlink(missing_ok=True)
  sail=command([args.sail,'--config',configpath,'--inst-limit',str(max(3000000,p['cases']*80)),'--show-times','--test-signature',out/'sail.sig','--signature-granularity','4',elf],args.timeout)
  (out/'sail.json').write_text(json.dumps(sail,indent=2)+'\n')
  result['sail_returncode']=sail['returncode']
 if spike['returncode']!=0 or not (out/'spike.sig').exists():return dict(result,status='spike_failed')
 cases=json.loads((src/'cases.json').read_text());order=json.loads((src/'order.json').read_text())
 rows={};errors=[]
 for model in ['spike','sail']:
  path=out/(model+'.sig')
  if not path.exists():continue
  data=signature(path)
  if len(data)!=64*len(cases):errors.append(f'{model}: signature length {len(data)}, expected {64*len(cases)}');continue
  rows[model]=[]
  with (out/(model+'.jsonl')).open('w') as f:
   for i,n in enumerate(order):
    b=data[i*64:(i+1)*64];words=struct.unpack('<16I',b)
    if words[7]!=n:errors.append(f'{model}: record {i} wrong ID {words[7]}, expected {n}')
    trap_pc=int.from_bytes(b[48:48+p['xlen']//8],'little')
    if words[6] and trap_pc!=targetpcs[n]:errors.append(f'{model}: case {n} setup/capture trap at {trap_pc:x}, target {targetpcs[n]:x}')
    misa=int.from_bytes(b[56:56+p['xlen']//8],'little')
    if p['bank']=='x' and misa&((1<<3)|(1<<5)|(1<<16)):errors.append(f'{model}: x-register profile unexpectedly advertises misa.F/D/Q')
    row=dict(id=n,result=b[:16].hex(),fcsr=words[4],fs=words[5],exception=words[6],memory=b[32:48].hex(),trap_pc=hex(trap_pc),misa=hex(misa))
    rows[model].append(row);f.write(json.dumps(row)+'\n')
 diffs=[];fsdiffs=[];traps={}
 if 'spike' in rows:
  for row in rows['spike']:traps[str(row['exception'])]=traps.get(str(row['exception']),0)+1
 if set(rows)=={'spike','sail'}:
  for a,b in zip(rows['spike'],rows['sail']):
   changes={k:[a[k],b[k]] for k in ['result','fcsr','exception','memory'] if a[k]!=b[k]}
   if changes:diffs.append(dict(case=cases[a['id']],differences=changes))
   if a['fs']!=b['fs']:fsdiffs.append(dict(id=a['id'],op=cases[a['id']]['op'],spike=a['fs'],sail=b['fs']))
  result.update(status='compared',differences=len(diffs),fs_policy_differences=len(fsdiffs),compared=len(rows['spike']))
 else:result.setdefault('status','sail_failed')
 result['spike_exceptions']=traps;result['harness_errors']=errors[:100];result['harness_error_count']=len(errors)
 if 'sail' in rows and 'SUCCESS' not in sail['stdout']:
  errors.append('Sail did not report HTIF SUCCESS; instruction-limit termination is not completion')
  result['harness_errors']=errors[:100];result['harness_error_count']=len(errors)
 if errors:result['status']='harness_failed'
 (out/'differences.json').write_text(json.dumps(diffs,indent=2)+'\n')
 (out/'fs-differences.json').write_text(json.dumps(fsdiffs,indent=2)+'\n')
 (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
 print(name,result['status'],'diff',len(diffs),'harness errors',len(errors),flush=True)
 return result

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--profiles',nargs='*');ap.add_argument('--spike',default=shutil.which('spike'));ap.add_argument('--sail',type=Path,default=DEFAULT_SAIL);ap.add_argument('--cc',default=shutil.which('riscv64-unknown-elf-gcc'));ap.add_argument('--nm',default=shutil.which('riscv64-unknown-elf-nm'));ap.add_argument('--timeout',type=int,default=600);ap.add_argument('--jobs',type=int,default=2);args=ap.parse_args()
 schema=json.loads(subprocess.check_output([str(args.sail),'--print-config-schema'],text=True))
 args.sail_has_q='Q' in schema['properties']['extensions']['properties']
 (ROOT/'results'/'capabilities.json').write_text(json.dumps(dict(sail_q=args.sail_has_q,sail_extensions=sorted(schema['properties']['extensions']['properties']),zdinx_helper_workaround='D.supported=true, F.supported=false; assert misa.F/D/Q=0 in every record'),indent=2)+'\n')
 profiles=json.loads((ROOT/'generated'/'profiles.json').read_text())
 if args.profiles:profiles={k:profiles[k] for k in args.profiles}
 env={'spike':command([args.spike,'--help']), 'sail':command([args.sail,'--build-info']), 'gcc':command([args.cc,'--version']), 'binaries':{str(path):hashlib.sha256(Path(path).read_bytes()).hexdigest() for path in [args.spike,args.sail,args.cc]}}
 (ROOT/'results'/'environment.json').write_text(json.dumps(env,indent=2)+'\n')
 with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
  results=list(pool.map(lambda item:run_profile(*item,args),profiles.items()))
 summary=dict(profiles=results,compared=sum(x.get('compared',0) for x in results),differences=sum(x.get('differences',0) for x in results),fs_policy_differences=sum(x.get('fs_policy_differences',0) for x in results))
 (ROOT/'results'/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
 return 1 if any(x.get('harness_error_count',0) or x.get('differences',0) or x['status'] in ['build_failed','spike_failed','sail_failed'] for x in results) else 0
if __name__=='__main__':raise SystemExit(main())
