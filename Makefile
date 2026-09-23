.PHONY: check

check:
	PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
	git diff --check
