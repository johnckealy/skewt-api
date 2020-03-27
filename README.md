# Flask-api-Heroku

####A flask template for creating a heroku RESTful API.

This is a template for creating an API in flask, a reference starting point that has the ability to connect to a PostgreSQL database in both development and production.


#####Usage

This is a basic skeleton, not even a crud app, for getting PostgreSQL database to work on both a dev and prod environment. Click the link to add an email to the database from a random sample of four emails.


#####Setting up – development

On your local server, you'll need to create the database and a virtual environment. For the venv, the key thing is to add everything you'll use into a requirements.txt file, so that heroku can create one by itself. You can then .gitignore the venv folder after you create it.

As for the database, you'll need to create it. You can use:

```
sudo -u my-postgres-role-name createdb database-name
```

Sometimes postgres will complain that your role has no password. If it does, you can create one by heading into the postgres console and trying

```
$ sudo -i -u postgres psql
psql (10.12 (Ubuntu 10.12-0ubuntu0.18.04.1))
Type "help" for help.

postgres=# ALTER USER <your role name> WITH PASSWORD 'a-great-password';
```

I have the dotenv library in my `requirements.txt`, it's a good idea to do the same, so that you can assign your environment variables.

Create a .env file, add it to your .gitignore (important!), and do something like:

```
PG_USER=my-postgres-role-name
PG_PWD=a-great-password
PG_DATABASE=database-name
FLASK_ENV=development
```

And then you can create the table(s) in the console using (remember to activate your venv):

```
$ python
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from app import db
>>> db.create_all()
>>> exit()


#####Setting up – production

I'm using Heroku's basic plan for this. [This](https://devcenter.heroku.com/articles/heroku-postgresql) page from the Heroku docs was quite useful.

```
$ # commit to git, then create the heroku app
$ heroku create <name of heroku app>
$
$ # You need to tell heroku to set up a postgres database
$ heroku addons:create heroku-postgresql:hobby-dev
$
$ git push heroku master
$
$ heroku run python                                                                     130 master!
Running python on ⬢ my-app... up, run.3634 (Free)
Python 3.6.10 (default, Dec 23 2019, 04:30:25)
[GCC 7.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from app import db
>>> db.create_all()
>>> exit()
```
