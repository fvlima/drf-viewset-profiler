clean: clean-eggs clean-build
	@find . -iname '*.pyc' -delete
	@find . -iname '*.pyo' -delete
	@find . -iname '*~' -delete
	@find . -iname '*.swp' -delete
	@find . -iname '__pycache__' -delete

clean-eggs:
	@find . -name '*.egg' -print0|xargs -0 rm -rf --
	@rm -rf .eggs/

clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info

deps: update
	poetry install -v

test: deps
	poetry run pytest -vvv test-drf-project/tests

build: test
	poetry build

release: clean build
	git rev-parse --abbrev-ref HEAD | grep '^master$$'
	git tag $(version)
	git push origin $(version)
	poetry publish

lint:
	pre-commit install && pre-commit run -a -v

pyformat:
	black .

update:
	poetry update