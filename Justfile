watch:
	poetry run ptw -- '--testmon'

test:
	poetry run pytest

format:
	poetry run black .
