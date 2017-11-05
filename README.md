# bjtu-sql
Software Project Training
## Setup of the Flask tutorial
### Needed
* virtualenv
* python3
* PostgreSQL
### Terminal commands
Commands to launch in the directory /flaskr
``` Shell Session
. venv/bin/activate
export FLASK_APP=flaskr
export FLASK_DEBUG=true
flask run
```
## Create a new virtual environment
* if there is already a virtual env, delete the folder venv ```rm -r venv```
* if the virtual env is one the root of folder flaskr try this command ```rm -r bin/ lib/ venv/lib```
``` Shell Session
virtualenv venv
. venv/bin/activate
pip install --editable .
pip install psycopg2
pip install flask-bcrypt
```
## Initiate the database
``` Shell Session
flask initdb
```
## Create a new user and a new database on postgreSQL
``` Shell Session
sudo -u postgres createuser gyf
sudo -u postgres createdb weibodb
sudo -u postgres psql
alter user gyf with encrypted password '123456';
grant all privileges on database weibodb to gyf;
\q
```
This will call the function `@app.cli.command('initdb') def initdb_command():` in the file `flaskr/flaskr.py`.
The function read the content of the file `schema.sql` and execute it on the database.
## Useful link
* https://wiki.evolix.org/HowtoPostgreSQL (list of useful commands in postgreSQL)
* https://wiki.postgresql.org/wiki/Psycopg2_Tutorial (Short tutorial of psycopg2)
* https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e (Create User and database for postgreSQL tutorial)