import os
from work_tracker.models.payroll_query import PayrollQueryModel
from work_tracker.models.timesheet import TimesheetModel
from flask import Flask, redirect, url_for, g, render_template, request, session
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
        g.timesheetModel = TimesheetModel(dbConn)
        g.payrollQueryModel = PayrollQueryModel(dbConn)

        staffID = session.get('staffID')
        if staffID:
            # TODO: Handle exception
            g.user = g.staffModel.getStaffMember(staffID)
        else:
            g.user = None

    @app.route("/", methods=["GET", "POST"])
    def signIn():
        # TODO: check if user is already signed in
        if g.user:
            # Already signed in
            return redirect(url_for('staff.homepage'))
        else:
            if request.method == 'POST':
                vaildCredentials = g.staffModel.signIn(
                    request.form['staffid'], request.form['password'])
                if vaildCredentials:
                    session['staffID'] = request.form['staffid']
                    return redirect(url_for('staff.homepage'))
                else:
                    failed = True
            else:
                failed = False

            return render_template('index-signIn.html', failed=failed)

    # Temp signout feature for debugging
    @app.route("/signout")
    def signOut():
        session['staffID'] = None
        return redirect(url_for('signIn'))

    return app
