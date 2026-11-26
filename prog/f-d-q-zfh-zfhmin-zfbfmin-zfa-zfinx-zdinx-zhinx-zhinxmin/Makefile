PYTHON ?= python3
JOBS ?= 3
TIMEOUT ?= 300
.PHONY: all generate run privilege report test
all:
	$(MAKE) generate
	$(MAKE) test
	$(MAKE) run
	$(MAKE) privilege
	$(MAKE) report
generate:
	$(PYTHON) generate.py --random 16
	$(PYTHON) edges.py
run:
	$(PYTHON) run.py --jobs $(JOBS) --timeout $(TIMEOUT)
privilege:
	$(PYTHON) privilege.py
report:
	$(PYTHON) analyze.py
test:
	$(PYTHON) test_reference.py
