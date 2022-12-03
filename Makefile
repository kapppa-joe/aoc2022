test:
	ptw -- '--testmon'

test_all:
	pytest

format:
	black .
