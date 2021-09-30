install:
	@poetry install
	@poetry run pre-commit install -f

test:
	@poetry run pytest -v -x -p no:warnings --cov-report term-missing --cov=./junito

ci:
	@poetry run pytest --cov=./junito

format:
	@poetry run black .

pre-commit:
	@poetry run pre-commit run --all

action:
	docker build --tag=junito:dev . && docker run junito:dev "./tests/fixtures/test-report.xml" "true" "false"
