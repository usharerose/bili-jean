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

clean-pyc:
	# clean all pyc files
	find . -name '__pycache__' | xargs rm -rf | cat
	find . -name '*.pyc' | xargs rm -f | cat

clean-container:
	# stop and remove useless containers
	docker-compose down --remove-orphans
