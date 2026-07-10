import os
from functools import wraps

from flask import Flask, redirect, render_template, request, session, url_for
from sqlalchemy.exc import SQLAlchemyError

from models import AdminUser, Incident, Service, db

INCIDENT_STATUSES = ["Operational", "Degraded", "Down"]

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    app.instance_path, "app.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)

    return wrapped_view

os.makedirs(app.instance_path, exist_ok=True)
db.init_app(app)

with app.app_context():
    db.create_all()

    if Service.query.count() == 0:
        db.session.add_all(
            [
                Service(name="Website", status="Operational"),
                Service(name="API", status="Operational"),
                Service(name="Database", status="Operational"),
            ]
        )
        db.session.commit()

    if AdminUser.query.filter_by(username="admin").first() is None:
        admin_user = AdminUser(username="admin")
        admin_user.set_password("admin123")
        db.session.add(admin_user)
        db.session.commit()


@app.route("/")
def index():
    try:
        services = Service.query.order_by(Service.name).all()
        incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    except SQLAlchemyError:
        app.logger.exception("Failed to load homepage data")
        return render_template(
            "error.html",
            message="We couldn't load the status page right now. Please try again shortly.",
        ), 500

    return render_template("index.html", services=services, incidents=incidents)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        try:
            admin_user = AdminUser.query.filter_by(username=username).first()
        except SQLAlchemyError:
            app.logger.exception("Failed to look up admin user")
            return render_template(
                "error.html",
                message="We couldn't process your login right now. Please try again shortly.",
            ), 500
        if admin_user and admin_user.check_password(password):
            session["logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        error = "Invalid username or password."
    return render_template("admin_login.html", error=error)


@app.route("/admin/logout")
def admin_logout():
    session.pop("logged_in", None)
    return redirect(url_for("admin_login"))


@app.route("/admin/dashboard", methods=["GET", "POST"])
@login_required
def admin_dashboard():
    form_data = {"title": "", "description": "", "service_id": "", "status": ""}
    error = None

    try:
        services = Service.query.order_by(Service.name).all()

        if request.method == "POST":
            title = request.form.get("title", "").strip()
            description = request.form.get("description", "").strip()
            service_id = request.form.get("service_id", "")
            status = request.form.get("status", "")

            form_data = {
                "title": title,
                "description": description,
                "service_id": service_id,
                "status": status,
            }

            service = Service.query.get(service_id) if service_id else None

            if not title:
                error = "Title cannot be empty."
            elif not description:
                error = "Description cannot be empty."
            elif not service:
                error = "Please select a valid service."
            elif status not in INCIDENT_STATUSES:
                error = "Status must be one of Operational, Degraded, or Down."
            else:
                incident = Incident(
                    title=title,
                    description=description,
                    status=status,
                    service_id=service.id,
                )
                db.session.add(incident)
                service.status = status
                db.session.commit()
                return redirect(url_for("admin_dashboard"))

        incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    except SQLAlchemyError:
        db.session.rollback()
        app.logger.exception("Failed to load or update dashboard data")
        return render_template(
            "error.html",
            message="We couldn't load the admin dashboard right now. Please try again shortly.",
        ), 500

    return render_template(
        "admin_dashboard.html",
        services=services,
        incidents=incidents,
        incident_statuses=INCIDENT_STATUSES,
        form_data=form_data,
        error=error,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
