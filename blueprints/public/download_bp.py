from flask import Blueprint, render_template, send_file, url_for

download_bp = Blueprint("download_bp", __name__)


@download_bp.route("/", methods=["GET"])
def get():
    return render_template("public/download.html"), 200


@download_bp.route("/insurance", methods=["GET"])
def insurance():
    return send_file(
        "static/pdf/W4lkies Proof of Cover.pdf",
        as_attachment=True,
        download_name="W4lkies Proof of Cover.pdf",
        mimetype="application/pdf",
    )


@download_bp.route("/welcome-pack", methods=["GET"])
def welcome_pack():
    return send_file(
        "static/pdf/flyer/W4lkies Welcome Pack.pdf",
        as_attachment=True,
        download_name="W4lkies Welcome Pack.pdf",
        mimetype="application/pdf",
    )


@download_bp.route("/flyer", methods=["GET"])
def flyer():
    return send_file(
        "static/pdf/flyer/W4lkies Flyer.pdf",
        as_attachment=True,
        download_name="W4lkies Flyer.pdf",
        mimetype="application/pdf",
    )


@download_bp.route("/business-card", methods=["GET"])
def business_card():
    return send_file(
        "static/pdf/W4lkies Business Card.pdf",
        as_attachment=True,
        download_name="W4lkies Business Card.pdf",
        mimetype="application/pdf",
    )
