# Pulp
Betting on Sports With Friends!

## Set Up

### Install requirements

### Make virtual environment
`virtualenv -p python3 venv`

### Source into virtual environment
`source venv/bin/activate`

#### Install Python Requirements
`pip install -r requirements`

#### Install Javascript Requirements
`yarn` (will install in /app/static/node_modules)

### Setup database
Make sure your local database is running and open it with
On a mac, to install postgresql:
`brew install postgres`

To start it and make it run in the background:
`brew services start postgresql`

Or, if you don't want/need a background service you can just run:
`pg_ctl -D /usr/local/var/postgres start`

To get into postgresql:
`psql postgres`

Create a new database with `CREATE DATABASE pulp`

`python db_create.py`

`python db_migrate.py`

### Create config
In the root directory, make a file called config.py using example_config.py as a template then replace all of the keys with your own

## Run the app
`python run.py`
