from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SelectField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, NumberRange

class ProductForm(FlaskForm):
    name = StringField(
        'Назва товару',
        validators=[
            DataRequired(message="Поле обов'язкове для заповнення"),
            Length(min=3, message="Назва повинна містити щонайменше 3 символи")
        ]
    )

    content = TextAreaField(
        'Опис товару',
        validators=[
            DataRequired(message="Поле обов'язкове для заповнення")
        ],
        render_kw={"rows": 5, "cols": 40}
    )

    price = DecimalField(
        'Ціна (грн)',
        places=2,
        validators=[
            DataRequired(message="Поле обов'язкове для заповнення"),
            NumberRange(min=0.01, message="Ціна повинна бути додатнім числом")
        ]
    )

    category = SelectField(
        'Категорія',
        choices=[
            ('', 'Оберіть категорію...'),
            ('electronics', 'Електроніка'),
            ('clothing', 'Одяг'),
            ('home', 'Товари для дому'),
            ('books', 'Книги')
        ],
        validators=[
            DataRequired(message="Оберіть категорію")
        ]
    )

    quantity = IntegerField(
        'Кількість одиниць',
        validators=[
            DataRequired(message="Поле обов'язкове для заповнення"),
            NumberRange(min=0, message="Кількість не може бути від'ємною")
        ]
    )

    image = FileField(
        'Зображення товару',
        validators=[
            FileAllowed(['jpg', 'jpeg', 'png'], message="Дозволені лише формати JPG, JPEG та PNG")
        ]
    )

    submit = SubmitField('Зберегти товар')