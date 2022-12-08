watch:
	poetry run ptw -- '--testmon'

test:
	poetry run pytest

format:
	poetry run black .

lint:
	poetry run pylint solutions tests