from flaskext.wtf import Form
from wtforms.fields import FileField, SubmitField, TextAreaField, TextField

class ChanForm(Form):
    """
    A basic ?chan-style form for both new threads and new replies.
    """

    name = TextField("Name", default="Anonymous")
    email = TextField("Email")
    subject = TextField("Subject")
    comment = TextAreaField("Comment")
    datafile = FileField("Image")
    submit = SubmitField("Submit")
