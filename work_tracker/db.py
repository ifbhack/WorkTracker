import sqlite3
import click
from flask import current_app, g, Flask
from flask.cli import with_appcontext

SCHEMA_FILENAME = "schema.sql"
TEST_DATA_FILENAME = "test_data.sql"

def getTestDatabase() -> sqlite3.Connection:
    """getTestDatabase for unit testing the model classes"""
    dbConn = sqlite3.connect(
            ":memory:",
            detect_types=sqlite3.PARSE_DECLTYPES
    )

    with open("work_tracker/schema.sql") as schemaFile:
        dbConn.executescript(schemaFile.read())

    return dbConn

def getDatabase() -> sqlite3.Connection:
    """getDatabase connection and load it into the flask application"""

    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def initialiseDatabase():
    """initialiseDatabase via schema file"""

    dbConn: sqlite3.Connection = getDatabase()

    with current_app.open_resource(SCHEMA_FILENAME) as schemaFile:
        dbConn.executescript(schemaFile.read().decode("utf8"))

    with current_app.open_resource(TEST_DATA_FILENAME) as schemaFile:
        dbConn.executescript(schemaFile.read().decode("utf8"))

@click.command('init-db')
@with_appcontext
def initialiseDatabaseCmd():
    """initialiseDatabase_cmd is a click command, call initialise_database instead"""

    initialiseDatabase()
    click.echo("database has been initialised")

def closeDatabase(err=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def prepareAppCallbacks(app: Flask):
    """prepareAppCallbacks to be called on certain events within flask"""

    # TODO: look into teardown_appcontext error handling
    app.teardown_appcontext(closeDatabase)
    app.cli.add_command(initialiseDatabaseCmd)
