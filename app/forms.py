from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp

class ContactForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(message="Поле обов'язкове для заповнення"),
            Length(min=4, max=10, message="Ім'я повинно містити від 4 до 10 символів")
        ]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Поле обов'язкове для заповнення"),
            Email(message="Введіть коректну електронну адресу")
        ]
    )

    phone = StringField(
        'Phone',
        validators=[
            DataRequired(message="Поле обов'язкове для заповнення"),
            Regexp(
                r'^\+380\d{9}$',
                message="Номер телефону має бути у форматі +380XXXXXXXXX (9 цифр після коду)"
            )
        ]
    )

    subject = SelectField(
        'Subject',
        choices=[
            ('', 'Оберіть тему звернення...'),
            ('tech_support', 'Технічна підтримка'),
            ('cooperation', 'Співпраця'),
            ('complaint', 'Скарга або пропозиція'),
            ('other', 'Інше')
        ],
        validators=[
            DataRequired(message="Будь ласка, оберіть тему")
        ]
    )

    message = TextAreaField(
        'Message',
        validators=[
            DataRequired(message="Поле обов'язкове для заповнення"),
            Length(max=500, message="Повідомлення не може перевищувати 500 символів")
        ]
    )

    submit = SubmitField('Send Message')