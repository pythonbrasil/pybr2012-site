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

setup: deps
	@python pythonbrasil8/manage.py syncdb
	@python pythonbrasil8/manage.py migrate
	@python pythonbrasil8/manage.py loaddata pythonbrasil8/fixtures/initial_data.json

run:
	@python pythonbrasil8/manage.py runserver 0.0.0.0:8000
