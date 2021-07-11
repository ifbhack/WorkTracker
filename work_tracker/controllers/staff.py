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


@bp.route("/calendar", methods=["GET"])
def calendar():
    return render_template('index-calendar.html')
