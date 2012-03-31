clean:
	@find . -name "*.pyc" -delete

deps:
	@pip install -r requirements.txt

test: deps clean
	@pythonbrasil8/manage.py test

jasminedeps: deps
	@pip install -r test_requirements.txt

jasmine: jasminedeps
	@jasmine-splinter -f `pwd`/pythonbrasil8/static_files/tests/jasmine/SpecRunner.html

