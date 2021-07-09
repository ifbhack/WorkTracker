import sqlite3
import click
from flask import current_app, g, Flask
from flask.cli import with_appcontext

SCHEMA_FILENAME = "schema.sql"
TEST_DATA_FILENAME = "test_data.sql"

def get_test_database() -> sqlite3.Connection:
    """get_test_database for unit testing the model classes"""
    db_conn = sqlite3.connect(
            ":memory:",
            detect_types=sqlite3.PARSE_DECLTYPES
    )

    with open("work_tracker/schema.sql") as schema_file:
        db_conn.executescript(schema_file.read())

    return db_conn

def get_database() -> sqlite3.Connection:
    """get_database connection and load it into the flask application"""

    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def initialise_database():
    """initialise_database via schema file"""

    db_conn: sqlite3.Connection = get_database()

    with current_app.open_resource(SCHEMA_FILENAME) as schema_file:
        db_conn.executescript(schema_file.read().decode("utf8"))

    with current_app.open_resource(TEST_DATA_FILENAME) as schema_file:
        db_conn.executescript(schema_file.read().decode("utf8"))

@click.command('init-db')
@with_appcontext
def initialise_database_cmd():
    """initialise_database_cmd is a click command, call initialise_database instead"""

    initialise_database()
    click.echo("database has been initialised")

def close_database(err=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def prepare_app_callbacks(app: Flask):
    """prepare_app_callbacks to be called on certain events within flask"""

    # TODO: look into teardown_appcontext error handling
    app.teardown_appcontext(close_database)
    app.cli.add_command(initialise_database_cmd)
