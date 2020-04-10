from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class getSection(FlaskForm):
    codesection = StringField('CodeSection', validators = [DataRequired()])
    submit = SubmitField('Submit')
    
class proceedNowTo86(FlaskForm):
    proceed = SubmitField('Proceed')
    
class proceed86to39(FlaskForm):
    proceed = SubmitField('Proceed')
    
class proceed39toPrior(FlaskForm):
    proceed = SubmitField('Proceed')
    
class proceedToNewSearch(FlaskForm):
    newsearch = SubmitField('New Search')
