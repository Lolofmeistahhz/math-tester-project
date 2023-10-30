from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, FileField
from wtforms.validators import DataRequired, Length, Regexp
from wtforms.widgets import TextArea


class LoginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired(message='Поле обязательно для заполнения'),Length(min=6, max=20)])
    password = PasswordField('password', validators=[DataRequired(message='Поле обязательно для заполнения'),Length(min=6, max=20)])
    submit = SubmitField('Вход')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, *kwargs)


class regForm(FlaskForm):
    login = StringField('login',
                        validators=[DataRequired(message='Поле обязательно для заполнения'), Length(min=6, max=20)])
    password = PasswordField('password', validators=[DataRequired(message='Поле обязательно для заполнения'),
                                                     Length(min=6, max=20)])
    confirm_password = PasswordField('password', validators=[DataRequired(message='Поле обязательно для заполнения'),
                                                             Length(min=6, max=20)])
    submit = SubmitField('Регистрация')

    def __init__(self, *args, **kwargs):
        super(regForm, self).__init__(*args, **kwargs)


class personalDataForm(FlaskForm):
    name = StringField('name',
                       validators=[DataRequired(message='Поле обязательно для заполнения'), Length(min=3, max=50)])
    surname = StringField('surname',
                          validators=[DataRequired(message='Поле обязательно для заполнения'), Length(min=3, max=50)])
    patronomyc = StringField('patronomyc', validators=[Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(message='Поле обязательно для заполнения'),
                                             Regexp(r'^[^@]+@[^@]+\.[^@]+$',
                                                    message='Адрес электронной почты должен содержать "@" и "."'),
                                             Length(min=5, max=100)
                                             ])
    school = StringField('school',
                         validators=[DataRequired(message='Поле обязательно для заполнения'), Length(min=1, max=120)])
    s_class = StringField('s_class',
                          validators=[DataRequired(message='Поле обязательно для заполнения'), Length(min=1, max=10)])
    s_teacher = StringField('s_teacher',
                            validators=[DataRequired(message='Поле обязательно для заполнения'), Length(min=3, max=60)])
    submit = SubmitField('Сохранить', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(personalDataForm, self).__init__(*args, **kwargs)


class editTest(FlaskForm):
    quest1 = StringField('quest1', validators=[DataRequired()])
    pic1 = FileField('pic1')
    answ1 = StringField('answ1', validators=[DataRequired(), Length(max=255)])
    quest2 = StringField('quest2', validators=[DataRequired()])
    pic2 = FileField('pic2')
    answ2 = StringField('answ2', validators=[DataRequired(), Length(max=255)])
    quest3 = StringField('quest3', validators=[DataRequired()])
    pic3 = FileField('pic3')
    answ3 = StringField('answ3', validators=[DataRequired(), Length(max=255)])
    quest4 = StringField('quest4', validators=[DataRequired()])
    pic4 = FileField('pic4')
    answ4 = StringField('answ4', validators=[DataRequired(), Length(max=255)])
    quest5 = StringField('quest5', validators=[DataRequired()])
    pic5 = FileField('pic5')
    answ5 = StringField('answ5', validators=[DataRequired(), Length(max=255)])
    quest6 = StringField('quest6', validators=[DataRequired()])
    pic6 = FileField('pic6')
    answ6 = StringField('answ6', validators=[DataRequired(), Length(max=255)])
    quest7 = StringField('quest7', validators=[DataRequired()])
    pic7 = FileField('pic7')
    answ7 = StringField('answ7', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Изменить')

    def __init__(self, *args, **kwargs):
        super(editTest, self).__init__(*args, **kwargs)
