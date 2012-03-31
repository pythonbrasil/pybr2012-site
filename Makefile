clean:
	@find . -name "*.pyc" -delete

deps:
	pip install -r requirements.txt

test: deps clean
	pythonbrasil8/manage.py test

