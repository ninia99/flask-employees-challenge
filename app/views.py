import json
from flask import Blueprint
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import func

from app.models import Employee
from app.schemas import EmployeeSchema, UpdateEmployeeSchema

bp = Blueprint("employees", __name__)


@bp.route('/employees', methods=["GET", "POST"])
@bp.route('/employees/<int:empl_id>', methods=["GET", "PUT", "DELETE"])
def get_employees(empl_id=None):
    if request.method == "GET":
        if empl_id:
            employee = Employee.query.get_or_404(empl_id)
            es = EmployeeSchema()
            return jsonify({'results': es.dump(employee)}), 200

        es = EmployeeSchema(many=True)
        employees = Employee.query.all()
        return jsonify({'results': es.dump(employees)}), 200
    if request.method == "POST":
        try:
            data = json.loads(request.data)
            employee = EmployeeSchema().load(data)
        except ValidationError as err:
            return jsonify(err.messages), 400
        except Exception as e:
            return jsonify({'message': f'invalid request {e}'}), 400
        empl = Employee(**employee).save()
        return jsonify({'results': {'id': empl.id}}), 201
    if request.method == "PUT":
        try:
            data = json.loads(request.data)
            employee = UpdateEmployeeSchema().load(data)
        except ValidationError as err:
            return jsonify(err.messages), 400
        except Exception as e:
            return jsonify({'message': f'invalid request {e}'}), 400
        Employee.query.filter_by(id=empl_id).update(employee)
        Employee.commit()
        return jsonify(), 204
    if request.method == "DELETE":
        empl = Employee.query.get_or_404(empl_id)
        empl.delete()
        return jsonify(), 204


@bp.route('/departments', methods=["GET"])
@bp.route('/departments/<string:name>', methods=["GET"])
def departments(name=None):
    if name:
        empls = Employee.query.filter_by(department=name).all()
        es = EmployeeSchema(many=True)
        return jsonify({'results': es.dump(empls)}), 200
    deps = Employee.query.with_entities(
        Employee.department
    ).distinct('department').all()
    return jsonify({'results': [i[0] for i in deps]}), 200


@bp.route('/average_salary/<string:department>', methods=["GET"])
def average_salary(department):
    avg_salary = Employee.query.filter_by(
        department=department
    ).with_entities(
        func.avg(Employee.salary)
    ).all()
    if average_salary:
        return jsonify({'average_salary': avg_salary[0][0]}), 200
    return jsonify({'average_salary': None}), 200


@bp.route('/top_earners', methods=["GET"])
def get_top_earners():
    emps = Employee.query.order_by(Employee.salary.desc()).limit(10).all()
    es = EmployeeSchema(many=True)
    return jsonify({"results": es.dump(emps)}), 200


@bp.route('/most_recent_hires', methods=["GET"])
def get_most_recent_hired():
    employees = Employee.query.order_by(
        Employee.hire_date.desc()
    ).limit(10).all()
    es = EmployeeSchema(many=True)
    return jsonify({"results": es.dump(employees)}), 200
