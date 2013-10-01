# These targets are not files
.PHONY: install upgrade sandbox demo coverage ci i18n lint travis docs

install:
	pip install -r requirements.txt --use-mirrors
	python setup.py develop

upgrade:
	pip install --upgrade -r requirements.txt --use-mirrors
	python setup.py develop --upgrade

sandbox: install
	-rm sandbox/db.sqlite
	sandbox/manage.py syncdb --noinput
	sandbox/manage.py migrate
	sandbox/manage.py loaddata sandbox/fixtures/auth.json countries.json
	sandbox/manage.py oscar_import_catalogue sandbox/fixtures/books-catalogue.csv

css:
	# Compile CSS files from LESS
	lessc oscar/static/oscar/less/styles.less > oscar/static/oscar/css/styles.css
	lessc oscar/static/oscar/less/responsive.less > oscar/static/oscar/css/responsive.css
	lessc oscar/static/oscar/less/dashboard.less > oscar/static/oscar/css/dashboard.css


clean:
	# Remove files not in source control
	find . -type f -name "*.pyc" -delete
	rm -rf nosetests.xml coverage.xml htmlcov *.egg-info *.pdf dist violations.txt
