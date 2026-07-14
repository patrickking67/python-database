import os
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Numeric(12, 2), nullable=False)

    def __repr__(self):
        return f"<Employee {self.name}>"


def create_app(test_config=None):
    app = Flask(__name__)
    database_path = Path(app.instance_path) / "employees.db"
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "development-only"),
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "DATABASE_URL", f"sqlite:///{database_path}"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)

    @app.get("/")
    def home():
        employee_count = db.session.scalar(db.select(db.func.count(Employee.id)))
        return render_template("home.html", employee_count=employee_count)

    @app.get("/employees")
    def view_employees():
        employees = db.session.scalars(db.select(Employee).order_by(Employee.name)).all()
        return render_template("view_employees.html", employees=employees)

    @app.route("/employees/new", methods=["GET", "POST"])
    def add_employee():
        if request.method == "POST":
            values, error = validate_employee(request.form)
            if error:
                flash(error, "error")
                return render_template("add_employee.html", values=request.form), 400

            db.session.add(Employee(**values))
            db.session.commit()
            flash(f"Added {values['name']}.", "success")
            return redirect(url_for("view_employees"))

        return render_template("add_employee.html", values={})

    @app.route("/employees/<int:employee_id>/edit", methods=["GET", "POST"])
    def update_employee(employee_id):
        employee = db.get_or_404(Employee, employee_id)
        if request.method == "POST":
            values, error = validate_employee(request.form)
            if error:
                flash(error, "error")
                return render_template(
                    "update_employee.html", employee=employee, values=request.form
                ), 400

            employee.name = values["name"]
            employee.position = values["position"]
            employee.salary = values["salary"]
            db.session.commit()
            flash(f"Updated {employee.name}.", "success")
            return redirect(url_for("view_employees"))

        return render_template("update_employee.html", employee=employee, values={})

    @app.post("/employees/<int:employee_id>/delete")
    def delete_employee(employee_id):
        employee = db.get_or_404(Employee, employee_id)
        employee_name = employee.name
        db.session.delete(employee)
        db.session.commit()
        flash(f"Deleted {employee_name}.", "success")
        return redirect(url_for("view_employees"))

    with app.app_context():
        db.create_all()

    return app


def validate_employee(form):
    name = form.get("name", "").strip()
    position = form.get("position", "").strip()
    salary_text = form.get("salary", "").strip()

    if not name or not position or not salary_text:
        return None, "Name, position, and salary are required."
    if len(name) > 100 or len(position) > 100:
        return None, "Name and position must be 100 characters or fewer."

    try:
        salary = round(float(salary_text), 2)
    except ValueError:
        return None, "Salary must be a number."

    if salary < 0 or salary > 999_999_999.99:
        return None, "Salary must be between 0 and 999,999,999.99."

    return {"name": name, "position": position, "salary": salary}, None


app = create_app()


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
