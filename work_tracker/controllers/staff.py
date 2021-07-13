from flask import Blueprint, render_template, request, redirect, url_for, flash, g

bp = Blueprint("staff", __name__, url_prefix="/staff")

# TODO: Check if user is signed in before accessing pages

@bp.route("/homepage", methods=["GET"])
def homepage():
    return render_template('index.html')


@bp.route("/view_employees", methods=["GET"])
def view_employees():
    # TODO: add try/catch, for now fail hard
    staffMembers = g.staffModel.getStaffMembers()

    return render_template('index-view-employees.html', staffMembers=staffMembers)


@bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == 'POST':
        g.staffModel.createStaffMember(
            request.form['fname'],
            request.form['lname'],
            request.form['eaddress'],
            request.form['contact'],
            request.form['address1'] + ' ' + request.form['address2'],
            request.form['suburb'],
            request.form['postcode'],
            request.form['state'],
            request.form['dob'],
            request.form['level'])

    return render_template('index-create-employee.html')


@bp.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == 'POST':
        form = request.form

        g.staffModel.updateStaffMember(
            form['staffID'],
            form['fname'],
            form['lname'],
            form['eaddress'],
            form['contact'],
            form['address1'],
            form['suburb'],
            form['postcode'],
            form['state'],
            form['dob'],
            form['level']
        )

    # TODO: fix mess here
    staffID = request.args.get('staffID')
    if staffID is None:
        # Edit the current user
        staffID = g.user.staffID

    staffMember = g.staffModel.getStaffMember(staffID)

    return render_template('index-edit-employee.html', staffMember=staffMember)


# NOTE: For both availability and add_roster backends,
# request data is a array containing:
# dayName - can be Mon, Tues, Wed, Thurs, Fri, Sat, Sun

# startTime and endTime - value ranging from 0 - 8
# 0 represents 9am, 8 represents 5pm


@bp.route("/availability", methods=["GET", "POST"])
def availability():
    if request.method == "POST":
        # backend
        print(request.get_json())
    existingData = [{'dayName': 'Sat', 'startTime': 0, 'duration': 4}, {'dayName': 'Sun', 'startTime': 0, 'duration': 3}]
    return render_template('index-calendar.html', existingData=existingData)


@bp.route("/add_roster", methods=["GET", "POST"])
def addRoster():
    if request.method == "POST":
        # backend
        print(request.get_json())
        print(request.args.get("staffID"))
    existingData = [{'dayName': 'Sat', 'startTime': 0, 'duration': 4}, {'dayName': 'Sun', 'startTime': 0, 'duration': 1}]
    return render_template('index-calendar.html', existingData=existingData)


@bp.route("/payroll_query", methods=["GET", "POST"])
def payrollQuery():
    if request.method == "POST":
        # backend
        print(request.get_json())
        print(request.args.get("staffID"))
    existingData = [{'dayName': 'Sat', 'startTime': 3, 'duration': 4}, {'dayName': 'Sun', 'startTime': 0, 'duration': 1}]
    return render_template('index-calendar.html', existingData=existingData, showChanges=True)
