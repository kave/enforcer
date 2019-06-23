circleci := ${CIRCLECI}
current_dir := $(shell pwd)
image_name := $(shell git remote show origin | grep -e 'Push.*URL.*github.com' | rev | cut -d '/' -f 1 | rev | cut -d '.' -f 1)

lint:
	@flake8 . --ignore=F403 &&\
		python -m pip install pip-licenses &&\
		(cat .licenseignore | sed 's/^[[:space:]]*$$/__nonexistent__/' > /tmp/licenseignore) &&\
		pip-licenses | grep -vf /tmp/licenseignore | (! grep -w GPL)

test:
	$(MAKE) lint
	tox

install:
	python setup.py develop

release:
	@python setup.py sdist bdist_wheel upload -r local

clean:
	@find . -name '*.pyc' -exec rm -f {} \;
	@find . -name '__pycache__' -exec rm -rf {} \;
	@find . -name 'Thumbs.db' -exec rm -f {} \;
	@find . -name '*~' -exec rm -f {} \;