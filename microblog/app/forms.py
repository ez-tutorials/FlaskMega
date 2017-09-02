
"""
from flask_wtf import Form
"flask_wtf.Form" has been renamed to "FlaskForm" and will be removed in 1.0.
"""
from flask_wtf import FlaskForm as Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length
"""
The DataRequired import is a validator, a function that can be attached to a field to perform validation on the data submitted by the user. The DataRequired validator simply checks that the field is not submitted empty.
"""
class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class EditForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

    """
    The form constructor now takes a new argument original_nickname. The validate method uses it to determine if the nickname has changed or not. If it hasn't changed then it accepts it. If it has changed, then it makes sure the new nickname does not exist in the database.
    """
    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user != None:
            self.nickname.errors.append(
                'This nickname is already in use. Please choose another one.')
            return False
        return True
