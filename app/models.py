from flask_login import UserMixin, login_manager

from app import db, app

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    usertype = db.Column(db.String(20), nullable=False)
    personal_info = db.relationship('UserPersonalInfo', backref='user', uselist=False)
    user_answers = db.relationship('User_answers', back_populates='user', uselist=False)

    def __repr__(self):
        return f'<User {self.id}>'

class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(500), nullable=False)
    tasks = db.relationship('TestTask', back_populates='test', lazy=True)
    test_results = db.relationship('Test_result', back_populates='test')

    def __repr__(self):
        return f'<Test {self.id}>'

class TestTask(db.Model):
    __tablename__ = 'testtask'
    id = db.Column(db.Integer, primary_key=True)
    Question = db.Column(db.String(500), nullable=False)
    picture = db.Column(db.String, nullable=True)
    Answer = db.Column(db.String(20), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    test = db.relationship('Test', back_populates='tasks')

    def __repr__(self):
        return f'<TestTask {self.id}>'

class Test_result(db.Model):
    __tablename__ = 'test_result'
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    grade = db.Column(db.Integer)
    date_time = db.Column(db.DateTime)
    test = db.relationship('Test', back_populates='test_results')
    user = db.relationship('User', backref='test_results')

    def __repr__(self):
        return f'<Test_result {self.id}>'

class User_answers(db.Model):
    __tablename__ = 'user_answers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('testtask.id'), nullable=True)
    answer = db.Column(db.String(20), nullable=False)
    is_answer_correct = db.Column(db.Boolean,nullable=False,default=False)
    user = db.relationship('User', back_populates='user_answers')
    task = db.relationship('TestTask', backref='user_answers')

    def __repr__(self):
        return f'<User_answers {self.id}>'


class TaskArchive(db.Model):
    __tablename__ = 'task_archive'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    pdf_file = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    teach_class = db.Column(db.String(10), nullable=False)


    def __repr__(self):
        return f'<TaskArchive {self.id}>'

class MUList(db.Model):
    __tablename__ = 'mulist'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    pdf_file = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    teach_class = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<MUList {self.id}>'

class UserPersonalInfo(db.Model):
    __tablename__ = 'user_personal_info'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    patronymic = db.Column(db.String(50), nullable=True)
    school = db.Column(db.String(120), nullable=False)
    s_class = db.Column(db.String(10), nullable=False)
    s_teacher = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f'<UserPersonalInfo {self.id}>'

with app.app_context():
    db.create_all()
