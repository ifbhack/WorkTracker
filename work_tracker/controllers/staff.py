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
            "password",
            request.form['contact'],
            request.form['address1'] + ' ' + request.form['address2'],
            request.form['suburb'],
            request.form['postcode'],
            request.form['state'],
            "2016-08-30",
            False)

    return render_template('index-edit-employee.html')
