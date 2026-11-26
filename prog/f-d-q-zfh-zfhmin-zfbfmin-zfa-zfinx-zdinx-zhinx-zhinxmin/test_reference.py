#!/usr/bin/env python3
import unittest
from fractions import Fraction
from reference import rounded,pow2,decode,NV,NX,UF,OF

class NumericalBoundaryTests(unittest.TestCase):
 def test_half_minimum_subnormal(self):
  self.assertEqual(rounded(pow2(-25),'h',0),(0,UF|NX))
  self.assertEqual(rounded(pow2(-25),'h',3),(1,UF|NX))
 def test_negative_underflow_keeps_sign(self):
  self.assertEqual(rounded(-pow2(-25),'h',0),(0x8000,UF|NX))
 def test_ties_even_and_ties_away(self):
  v=Fraction(1)+pow2(-11)
  self.assertEqual(rounded(v,'h',0),(0x3c00,NX))
  self.assertEqual(rounded(v,'h',4),(0x3c01,NX))
 def test_exact_minimum_and_maximum(self):
  self.assertEqual(rounded(pow2(-24),'h',0),(1,0))
  self.assertEqual(rounded(Fraction(65504),'h',0),(0x7bff,0))
 def test_overflow(self):
  self.assertEqual(rounded(Fraction(65536),'h',0),(0x7c00,OF|NX))
  self.assertEqual(rounded(Fraction(65536),'h',1),(0x7bff,OF|NX))
 def test_unbounded_square_root(self):
  self.assertEqual(rounded(Fraction(4),'s',0,sqrt=True),(0x40000000,0))
  self.assertEqual(rounded(Fraction(2),'s',0,sqrt=True),(0x3fb504f3,NX))
 def test_binary128_not_host_float(self):
  v=Fraction(1)+pow2(-112)
  raw,flags=rounded(v,'q',0)
  self.assertEqual(flags,0)
  self.assertEqual(decode(raw,'q')[2],v)
 def test_source_exponent_is_not_destination_exponent(self):
  self.assertEqual(decode(255<<52,'d')[2],pow2(-768))
 def test_tininess_after_rounding(self):
  # Tininess uses its own unbounded-exponent rounding (README §6.1, Unpriv. §25.3.2.6.1):
  # a tiny exact value can be delivered as MIN_NORM and still signal UF.
  self.assertEqual(rounded(pow2(-126)-3*pow2(-152),'s',0),(0x00800000,UF|NX))
  # An exact value just below MIN_NORM whose unbounded rounding reaches MIN_NORM is not tiny.
  # RUP rounds it (both roundings) to MIN_NORM, so only NX is set.
  self.assertEqual(rounded(pow2(-126)-pow2(-151),'s',4),(0x00800000,NX))
if __name__=='__main__':unittest.main()
