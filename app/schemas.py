from marshmallow import fields

from . import ma
from app.models import Employee


class EmployeeSchema(ma.SQLAlchemySchema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    department = fields.Str(required=True)
    salary = fields.Float(required=True)
    hire_date = fields.DateTime(required=True)

    class Meta:
        model = Employee
        fields = ('id', 'name', 'department', 'salary', 'hire_date')


class UpdateEmployeeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Employee
        fields = ('name', 'department', 'salary', 'hire_date')
