install:
	pip install -r requirements.txt --use-mirrors
	python setup.py develop

upgrade:
	pip install -U -r requirements.txt --use-mirrors
	python setup.py develop --upgrade

sandbox: install
    -rm -f sandbox/db.sqlite
    # Create database
    sandbox/manage.py syncdb --noinput
    sandbox/manage.py migrate
    # Import some fixtures
    sandbox/manage.py oscar_import_catalogue sandbox/fixtures/*.csv
    sandbox/manage.py oscar_import_catalogue_images sandbox/fixtures/images.tar.gz
    sandbox/manage.py loaddata countries.json _fixtures/pages.json _fixtures/auth.json _fixtures/ranges.json _fixtures/offers.json
    sandbox/manage.py clear_index --noinput
    sandbox/manage.py update_index catalogue
