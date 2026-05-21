from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Username cannot be blank."),
            Length(min=4, message="Username must be greater than 3 characters.")
        ]
    )

    pwd = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password cannot be blank.")
        ]
    )

    pwd_confirm = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(message="Password confirm cannot be blank."),
            EqualTo("pwd", message="Passwords don't match.")
        ]
    )