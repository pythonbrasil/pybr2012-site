clean:
	@find . -name "*.pyc" -delete

deps:
	@pip install -r requirements.txt

test: deps clean
	@python manage.py test

jasminedeps: deps
	@pip install -r test_requirements.txt

jasmine: jasminedeps
	@jasmine-splinter -f `pwd`/pythonbrasil8/static_files/tests/jasmine/SpecRunner.html

setup: deps
	@python manage.py syncdb
	@python manage.py migrate
	@python manage.py loaddata pythonbrasil8/fixtures/initial_data.json

settings:
	cp pythonbrasil8/settings_local.py{.example,}

run:
	@python manage.py runserver 0.0.0.0:8000
