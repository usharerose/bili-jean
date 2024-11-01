.PHONY: clean-pyc

build: clean-pyc
	docker-compose build bili-jean-build

run: build clean-container
	docker-compose up -d bili-jean-run

ssh:
	docker-compose exec bili-jean-run /bin/sh

lint:
	python -m flake8 bili_jean/

lintd: build clean-container
	docker-compose up --exit-code-from bili-jean-lint bili-jean-lint

type-hint:
	python -m mypy bili_jean/

type-hintd: build clean-container
	docker-compose up --exit-code-from bili-jean-type-hint bili-jean-type-hint

pretty:
	python -m autopep8 bili_jean/

test:
	python -m pytest -sv --cov-report term-missing --cov-report html:coverage_report --cov-report xml:coverage_report/cov.xml --junitxml=coverage_report/pytest.xml --cov=bili_jean/ --disable-warnings -p no:cacheprovider tests/*

testd: build clean-container
	docker-compose up --exit-code-from bili-jean-test bili-jean-test

clean-pyc:
	# clean all pyc files
	find . -name '__pycache__' | xargs rm -rf | cat
	find . -name '*.pyc' | xargs rm -f | cat

clean-container:
	# stop and remove useless containers
	docker-compose down --remove-orphans
