from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateTimeLocalField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length
from app import db

CATEGORIES = [
    ("news", "News"),
    ("publication", "Publication"),
    ("tech", "Tech"),
    ("other", "Other"),
]


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2, max=150)])
    content = TextAreaField(
        "Content", validators=[DataRequired()], render_kw={"rows": 5, "cols": 40}
    )
    is_active = BooleanField("Active Post", default=True)
    publish_date = DateTimeLocalField(
        "Publish Date", format="%Y-%m-%dT%H:%M", default=datetime.now
    )
    category = SelectField("Category", choices=CATEGORIES, validators=[DataRequired()])
    author_id = SelectField("Author", coerce=int, validators=[DataRequired()])
    tags = SelectMultipleField("Tags", coerce=int)
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from app.posts.models import Tag
        from app.users.models import User

        authors = db.session.scalars(db.select(User).order_by(User.id)).all()
        self.author_id.choices = [(author.id, author.username) for author in authors]

        all_tags = db.session.scalars(db.select(Tag).order_by(Tag.id)).all()
        self.tags.choices = [(tag.id, tag.name) for tag in all_tags]