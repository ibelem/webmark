from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, DateTimeField, RadioField
from wtforms.validators import DataRequired, Length, Email, Regexp, URL
from flask_wtf.file import FileField, FileAllowed
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User, Webmark
from datetime import datetime
from .. import db
from flask_sqlalchemy import get_debug_queries
from sqlalchemy import func, or_, and_


class FeedbackForm(FlaskForm):
    email = StringField('Contact (*)', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    title = StringField('Title', validators=[DataRequired(), Length(0, 256)])
    details = TextAreaField('Details', validators=[Length(max=20480)])
    submit = SubmitField('Submit')

class WebMarkProposalForm(FlaskForm):
    name = StringField('Benchmark Name (*)', validators=[DataRequired(), Length(1, 128)])
    email = StringField('Contact (*)', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    url = StringField('URL', validators=[Length(0, 1024)])
    details = TextAreaField('Details', validators=[Length(max=20480)])
    submit = SubmitField('Submit')


class WebMarkProposalReviewForm(FlaskForm):
    reviewed = RadioField('', choices=[(True, 'Reviewed'), (False, 'Not Reviewed')])
    added = RadioField('', choices=[(True, 'Added'), (False, 'Not Added')])
    submit = SubmitField('Submit')


class WebMarkForm(FlaskForm):
    name = StringField('Name (*)', validators=[DataRequired(), Length(1, 128)])
    metrics = StringField('Score Metrics (*) (e.g. Bigger scores are better)', validators=[DataRequired(), Length(1, 64)])
    tags = StringField('Tags (*) (Split with comma, semicolon or blank)', validators=[DataRequired(), Length(1, 128)])
    # ready = BooleanField('Ready for Automation Test')
    # duration = StringField('Test Duration', validators=[Length(0, 32)])
    version = StringField('Version', validators=[Length(0, 32)])
    license = StringField('License', validators=[Length(0, 32)])
    developed_by = StringField('Developed By', validators=[Length(0, 64)])
    screenshot_path = FileField('Screenshot (jpg, png)', validators=[
        # FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only, jpg or png files are allowed.')
    ])
    url = StringField('URL', validators=[Length(0, 1024)])
    repo_url = StringField('Repo URL', validators=[Length(0, 1024)])
    summary = StringField('Summary', validators=[Length(0, 256)])
    details = TextAreaField('Details', validators=[Length(max=20480)])
    pros = TextAreaField('Pros', validators=[Length(max=20480)])
    cons = TextAreaField('Cons/Notes', validators=[Length(max=20480)])
    submit = SubmitField('Submit')

    def validate_name(self, field):
        if Webmark.query.filter_by(name=field.data).first():
            raise ValidationError('Webmark name ' + field.data + ' already in use.')


class EditWebMarkForm(FlaskForm):
    name = StringField('Name (*)', validators=[DataRequired(), Length(1, 128)])
    metrics = StringField('Score Metrics (*) (e.g. Bigger scores are better)', validators=[DataRequired(), Length(1, 64)])
    tags = StringField('Tags (*)', validators=[DataRequired(), Length(1, 128)])
    version = StringField('Version', validators=[Length(0, 32)])
    license = StringField('License', validators=[Length(0, 32)])
    developed_by = StringField('Developed By', validators=[Length(0, 64)])
    screenshot_path = FileField('Screenshot (jpg, png / 708x472)', validators=[
        # FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only, jpg or png files are allowed.')
    ])
    url = StringField('URL', validators=[Length(0, 1024)])
    repo_url = StringField('Repo URL', validators=[Length(0, 1024)])
    summary = StringField('Summary', validators=[Length(0, 256)])
    details = TextAreaField('Details', validators=[Length(max=20480)])
    pros = TextAreaField('pros', validators=[Length(max=20480)])
    cons = TextAreaField('cons', validators=[Length(max=20480)])
    submit = SubmitField('Submit')

    def __init__(self, id, *args, **kwargs):
        super(EditWebMarkForm, self).__init__(*args, **kwargs)
        self.id = id

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class PostForm(FlaskForm):
    body = PageDownField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    body = TextAreaField('Enter your comment', validators=[DataRequired()])
    submit = SubmitField('Submit')

class NewsForm(FlaskForm):
    forwebmark = SelectField('Add News/Updates for', coerce=int)
    summary = StringField('Summary (*)', validators=[DataRequired(), Length(1, 256)])
    details = TextAreaField('Description (*)', validators=[DataRequired(), Length(max=20480)])
    url = StringField('URL', validators=[Length(0, 1024)])
    source = StringField('News from', validators=[Length(0, 128)])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.forwebmark.choices = [(forwebmark.id, forwebmark.name)
                             for forwebmark in Webmark.query.order_by(Webmark.name).all()]



