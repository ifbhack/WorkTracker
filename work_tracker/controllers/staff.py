from flask import Blueprint, render_template, request, redirect, url_for, flash, g

bp = Blueprint("staff", __name__, url_prefix="/staff")

@bp.route("/view", methods=["GET"])
def view():
    # TODO: add try/catch, for now fail hard
    staffMembers = g.staffModel.getStaffMembers()

    # NOTE: quick hack for now just to display something in the view
    g.user = staffMembers[0]
    return render_template('index-view-employees.html', staffMembers=staffMembers)


@bp.route("/edit", methods=["GET"])
def edit():
    # NOTE: Hack to get g.user working from view function
    staffMembers = g.staffModel.getStaffMembers()
    g.user = staffMembers[0]

    return render_template('index-edit-employee.html')
