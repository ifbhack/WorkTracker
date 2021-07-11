from flask import Blueprint, render_template, request, redirect, url_for, flash, g

bp = Blueprint("staff", __name__, url_prefix="/staff")


@bp.route("/view", methods=["GET"])
def view():
    # TODO: add try/catch, for now fail hard
    staffMembers = g.staffModel.getStaffMembers()

    # NOTE: quick hack for now just to display something in the view
    g.user = staffMembers[0]
    return render_template('index-view-employees.html', staffMembers=staffMembers)


@bp.route("/create", methods=["GET", "POST"])
def create():
    # NOTE: Hack to get g.user working from view function
    staffMembers = g.staffModel.getStaffMembers()
    g.user = staffMembers[0]

    if request.method == 'POST':
        g.staffModel.createStaffMember(
            # TODO: Fill out missing form data
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
    # NOTE: Hack to get g.user working from view function
    staffMembers = g.staffModel.getStaffMembers()
    g.user = staffMembers[0]

    # TODO: Edit other employees other than g.user
    # TODO: On submit, data is changed but fields contain old data
    if request.method == 'POST':
        staffMember = g.staffModel.getStaffMember(g.user.staffID)

        staffMember.firstName = request.form['fname']
        staffMember.lastName = request.form['lname']
        staffMember.email = request.form['eaddress']
        staffMember.contactNumber = request.form['contact']
        staffMember.address = request.form['address1']
        staffMember.suburb = request.form['suburb']
        staffMember.postcode = request.form['postcode']
        staffMember.state = request.form['state']
        staffMember.dob = request.form['dob']
        staffMember.isManager = request.form['level']

        g.staffModel.updateStaffMember(staffMember)

    return render_template('index-edit-employee.html')
