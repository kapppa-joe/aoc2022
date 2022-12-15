watch:
	poetry run ptw -- -- --testmon

test:
	poetry run pytest

format:
	poetry run black .

lint:
	poetry run pylint solutions tests

start_today:
	cp -n solutions/day_xx.py solutions/day_$(date +"%d").py && touch tests/day_$(date +"%d")_test.py


