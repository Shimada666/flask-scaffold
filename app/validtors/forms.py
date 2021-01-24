from flask import request
from wtforms import Form as WTForm, StringField, PasswordField
from wtforms.validators import DataRequired

from app.exceptions import IllegalArgumentException


class Form(WTForm):
    def __init__(self):
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        super(Form, self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(Form, self).validate()
        if not valid:
            raise IllegalArgumentException(msg=self.errors)
        return self

    @property
    def errors_info(self):
        errors_lst = []
        for k, v in self.errors.items():
            errors_lst += v
        errors_str = '\n'.join(errors_lst)
        return errors_str


# login validate
class LoginForm(Form):
    username = StringField(validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired(message='密码不可为空')])


# post validate
class CreateOrUpdatePost(Form):
    title = StringField(validators=[DataRequired()])
    content = StringField(validators=[DataRequired()])
