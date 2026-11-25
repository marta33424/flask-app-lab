from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError
from .models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Введіть ім'я користувача."),
            Length(min=3, max=20, message="Довжина має бути від 3 до 20 символів."),
            Regexp(
                r"^[A-Za-z][A-Za-z0-9._]*$",
                message="Ім'я користувача має починатися з літери і містити лише літери, цифри, крапки або підкреслення.",
            ),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Введіть електронну пошту."),
            Email(message="Введіть коректну адресу електронної пошти."),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Введіть пароль."),
            Length(min=6, message="Пароль має містити щонайменше 6 символів."),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(message="Підтвердіть пароль."),
            EqualTo("password", message="Паролі повинні збігатися."),
        ],
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError("Користувач з таким ім'ям уже існує.")

    def validate_email(self, email):
        existing_email = User.query.filter_by(email=email.data).first()
        if existing_email:
            raise ValidationError("Користувач з такою електронною поштою уже зареєстрований.")