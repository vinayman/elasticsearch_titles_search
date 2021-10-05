from wtforms import Form, IntegerField, StringField
from wtforms.validators import InputRequired, NumberRange


class SuggestForm(Form):
    q = StringField("q", validators=[InputRequired()])
    max_results = IntegerField(
        "max_results", validators=[NumberRange(min=1)], default=10
    )
