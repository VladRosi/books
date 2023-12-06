# Notes

## Install db user and db

```bash
(.venv) ➜  books createuser books_user
(.venv) ➜  books createdb books_db
(.venv) ➜  books dropdb books_db
(.venv) ➜  books createdb books_db -Obooks_user
(.venv) ➜  books pip install psycopg2
```

## Create SuperUser of psql and permissions for django to create and delete databases to do tests

```bash
createuser -s -P superadmin
psql --username=vlad_rosi books_db
=> ALTER USER books_user CREATEDB;
```

```bash
pip install coverage

coverage run --source='.' ./manage.py test .

coverage report

coverage html
```

```bash
pip install django-filter
```

. . .
Content-Type: application/x-www-form-urlencoded
. . .

. . .
pip install httpie
. . .

```bash
telnet python.org

ifconfig 

```
