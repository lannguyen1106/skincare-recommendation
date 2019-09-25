from functools import wraps

from flask_wtf import FlaskForm
from wtforms import FieldList, FloatField, StringField
from wtforms.validators import DataRequired, Optional


class SellForm(FlaskForm):
    """
    FlaskForm for selling items.
    """
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    price = FloatField('price', validators=[DataRequired()])
    image = StringField('image', validators=[DataRequired()])

def sell_form_validation_required(f):
    """
    A decorator for validating requests with the sell form.
    Returns an error message if validation fails.

    Parameters:
       f (func): The view function to decorate.

    Output:
       decorated (func): The decorated function.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        sell_form = SellForm()
        if not sell_form.validate():
            return 'Something does not look right. Check your input and try again.', 400

        return f(form=sell_form, *args, **kwargs)
    return decorated