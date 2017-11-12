# bjtu-sql
Software Project Training
## Setup of the Flask tutorial
### Needed
* virtualenv
* python3
* PostgreSQL
* pgcrypto on postgresql

### Terminal commands
Commands to launch in the directory /flaskr
``` Shell Session
. venv/bin/activate
python flaskr/flaskr/flaskr2.py
```

## Create a new virtual environment
* if there is already a virtual env, delete the folder venv ```rm -r venv```
* if the virtual env is one the root of folder flaskr try this command ```rm -r bin/ lib/ venv/lib```
``` Shell Session
virtualenv venv
. venv/bin/activate
pip install --editable .
pip install psycopg2
```

## Add pgcrypto on psql
``` Shell Session
sudo apt-get install postgresql-contrib libpq-dev
// Create the database first, then:
cd `pg_config --sharedir` // Move to the postgres directory that holds these scripts.
sudo echo "create extension pgcrypto" | sudo -u postgres psql -d weibodb // enable the pgcrypo extension
```
Now you can use pgcrypto in query.
###Use crypt() and gen_salt() in queries
Compare :pass to existing hash with:
``` SQL Session
select * from accounts where password_hash = crypt(:pass, password_hash);
//(note how the existing hash is used as its own individualized salt)
```
Create a hash of :password with a great random salt:
``` SQL Session
insert into accounts (password) values crypt(:password, gen_salt('bf', 8));
//(the 8 is the work factor)
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
Don't forget to install pgcrypto to the database
## Initiate the database
``` Shell Session
python flaskr/flaskr/sql.py
```
This will call the function `@app.cli.command('initdb') def initdb_command():` in the file `flaskr/flaskr.py`.
The function read the content of the file `schema.sql` and execute it on the database.
## Good uses
* if you want to give feedback, use flash('your error, messages', 'category'), the category parametres let you choose the color : primary, secondary, success, danger, warning, info, light, dark. Exemple of color here : https://getbootstrap.com/docs/4.0/components/alerts/#examples
* macros.html and form.html allow to create some kind of html template, if you want to do a form simply use forms.input() and forms.submit() instead of write complete html form.
* the result of cursor.fetchall() is a RawDict, you can use it as a dictionnary `result['key']`
** RawDict cannot be modified, if you need to modified it convert him into a real python dictionnary, like this: `new_result = dict(result.items())` 
** more info here : http://initd.org/psycopg/docs/extras.html#dictionary-like-cursor
## Useful link
* https://wiki.evolix.org/HowtoPostgreSQL (list of useful commands in postgreSQL)
* https://wiki.postgresql.org/wiki/Psycopg2_Tutorial (Short tutorial of psycopg2)
* https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e (Create User and database for postgreSQL tutorial)
* https://stackoverflow.com/questions/2647158/how-can-i-hash-passwords-in-postgresql (pqcrypto tutorial)
* http://jinja.pocoo.org/docs/2.9/templates/ (documentation of jinja2, html template)
