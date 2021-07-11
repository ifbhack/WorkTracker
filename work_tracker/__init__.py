import os
from flask import Flask, redirect, url_for, g, render_template, request
from work_tracker.models import StaffModel

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, "worktracker.db"),
    )

    from . import db
    db.prepareAppCallbacks(app)


    from .controllers import staffBP
    app.register_blueprint(staffBP)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.before_request
    def createModels():
        dbConn = db.getDatabase()
        g.staffModel = StaffModel(dbConn)
        # TODO: setup user sessions here

    @app.route("/")
    def signIn():
        # TODO: check if user is already signed in
        if request.method == 'POST':
            try:
                # TODO: sign user in, here we can check if a staff
                # member is a manager and redirect them to the appropriate blueprint
                # return render_template('index-home.html', name=g.user.name, isManager=g.user.isManager)
                return "Login"
            except Exception:
                return 'User Not Found'

        else:
            return render_template('index-signIn.html')


    return app
