find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
rm -rf db.sqlite3
