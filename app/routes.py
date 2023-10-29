import os
import tempfile
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, send_file
from flask_login import LoginManager, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from fpdf import FPDF
from PIL import Image as PILImage
from app import app, db
from app.forms import LoginForm, regForm, editTest, personalDataForm
from app.models import User, Test_result, Test, UserPersonalInfo, TestTask, User_answers, TaskArchive, MUList

Login_Manager = LoginManager(app)

user_menu = [
    {'name': 'Главная', 'url': '/index'},
    {'name': 'Авторизация', 'url': '/login'},
    {
        'name': 'Тестирование',
        'submenu': [
            {'name': '9 класс', 'url': '/test9c'},
            {'name': '10 класс', 'url': '/test10c'},
            {'name': '11 класс', 'url': '/test11c'}
        ]
    }, {'name': 'Методические указания', 'url': '/MUList'},
    {'name': 'Архив заданий', 'url': '/task_archive'}
]

admin_menu = [{'name': 'Главная', 'url': '/index'}, {
    'name': 'Тесты',
    'submenu': [
        {'name': '9 класс', 'url': '/admin/edit/9c'},
        {'name': '10 класс', 'url': '/admin/edit/10c'},
        {'name': '11 класс', 'url': '/admin/edit/11c'}
    ]
}, {'name': 'Результаты', 'url': '/admin/test_result'},
              {'name': 'Методические указания', 'url': '/admin/upload_MU'},
              {'name': 'Архив заданий', 'url': '/admin/upload_archive'},
              {'name': 'Выход', 'url': '/logout'}
              ]

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'app/static/images/'
UPLOAD_FOLDER_ARCHIVE = 'app/static/Archive/'
UPLOAD_FOLDER_MU = 'app/static/MU/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_ARCHIVE'] = UPLOAD_FOLDER_ARCHIVE
app.config['UPLOAD_FOLDER_MU'] = UPLOAD_FOLDER_MU
DOWNLOAD_FOLDER_ARCHIVE = '../app/static/Archive/'
DOWNLOAD_FOLDER_MU = '../app/static/MU/'
DOWNLOAD_FOLDER_CERTIFICATE = 'app/static/сertificates/'
FONT_PATH = 'app/static/fonts/DejaVuSans.ttf'
app.config['DOWNLOAD_FOLDER_ARCHIVE'] = DOWNLOAD_FOLDER_ARCHIVE
app.config['DOWNLOAD_FOLDER_MU'] = DOWNLOAD_FOLDER_MU
app.config['DOWNLOAD_FOLDER_CERTIFICATE'] = DOWNLOAD_FOLDER_CERTIFICATE


@Login_Manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        cur_u = User.query.filter(User.id == current_user.id).first()
        if cur_u.usertype == "Администратор":
            return render_template("index.html", menu=admin_menu, footer=True)
        elif cur_u.usertype == "Пользователь":
            return render_template("index.html", menu=user_menu, footer=True)
    else:
        return render_template("index.html", menu=user_menu, footer=True)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and check_password_hash(user.password, form.password.data):
            if user.usertype == "Администратор":
                login_user(user)
                return render_template('index.html', menu=admin_menu)
            else:
                login_user(user)
                return redirect(url_for('pd', menu=user_menu))
        else:
            flash("Неверный логин или пароль", "error")
    return render_template("login.html", FlaskForm=form, title="Авторизация", menu=user_menu, footer=True)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = regForm(request.form, crsf=True)
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if form.password.data == form.confirm_password.data:
            if not user:
                hashed_password = generate_password_hash(form.password.data)
                u = User(login=form.login.data, password=hashed_password, usertype="Пользователь")
                db.session.add(u)
                db.session.commit()
                return redirect(url_for('login'))
            elif user:
                flash("Данный логин уже занят!", "danger")
                return redirect(url_for('register'))
        else:
            flash("Введенные пароли не совпадают!", "danger")
            return redirect(url_for('register'))
    return render_template("register.html", FlaskForm=form, title="Регистрация", menu=user_menu, footer=True)


@app.route('/change_log_data', methods=['GET', 'POST'])
def change_log_data():
    form = regForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(login=current_user.login).first()
        if user and check_password_hash(user.password, form.password.data):
            flash('Новый пароль совпадает с текущим', 'warning')
        elif form.password.data != form.confirm_password.data:
            print("213")
            flash('введенные пароли не совпадают', 'warning')
        else:
            user.login = form.login.data
            hashed_password = generate_password_hash(form.password.data)
            user.password = hashed_password
            db.session.commit()
            logout_user()
            return render_template('index', menu=user_menu)
    return render_template('edit_log_pass.html', FlaskForm=form)


@app.route('/personal_data', methods=["GET", "POST"])
def pd():
    if current_user.is_authenticated:
        cur_u = User.query.filter(User.id == current_user.id).first()
        if cur_u.usertype == "Администратор":
            return render_template("index.html", menu=admin_menu, footer=True)
        else:
            user = UserPersonalInfo.query.filter(UserPersonalInfo.user_id == current_user.id).first()
            if user:
                return redirect(url_for('index'))
            form = personalDataForm(request.form)
            if form.validate_on_submit():
                pd = UserPersonalInfo(
                    user_id=current_user.id,
                    surname=form.surname.data,
                    name=form.name.data,
                    email=form.email.data,
                    patronymic=form.patronomyc.data,
                    school=form.school.data,
                    s_class=form.s_class.data,
                    s_teacher=form.s_teacher.data
                )
                db.session.add(pd)
                db.session.commit()
                return redirect(url_for('index'))
    return render_template("personal_data.html", FlaskForm=form, title="Личные данные", menu=user_menu, footer=True)


@app.route('/edit/personal_data', methods=["GET", "POST"])
def edit_pd():
    if current_user.is_authenticated:
        cur_u = User.query.filter(User.id == current_user.id).first()
        if cur_u.usertype == "Администратор":
            return render_template("index.html", menu=admin_menu, footer=True)
        else:
            form = personalDataForm()
            if form.validate_on_submit():
                user = UserPersonalInfo.query.filter(UserPersonalInfo.user_id == current_user.id).first()
                user.name = form.name.data
                user.surname = form.surname.data
                user.email = form.email.data
                user.patronymic = form.patronomyc.data
                user.school = form.school.data
                user.s_class = form.s_class.data
                user.s_teacher = form.s_teacher.data
                db.session.commit()
                return redirect(url_for('profile', id=current_user.id))

    return render_template("personal_data.html", FlaskForm=form, title="Личные данные", menu=user_menu, footer=True)


@app.route('/logout')
def logout():
    logout_user()
    return render_template('index.html', menu=user_menu)


@app.route('/profile/<string:id>')
def profile(id):
    if current_user.is_authenticated:
        cur_u = User.query.filter(User.id == current_user.id).first()
        if cur_u.usertype == "Администратор":
            return render_template("index.html", menu=admin_menu, footer=True)
        else:
            user = UserPersonalInfo.query.filter(UserPersonalInfo.user_id == current_user.id).first()
            testdata9c = db.session.query(Test_result.grade, Test.Name, Test_result.date_time).filter(
                Test_result.user.has(id=current_user.id), Test_result.test.has(id=1), Test.id == 1).order_by(
                Test_result.date_time.desc()).limit(1)
            testdata10c = db.session.query(Test_result.grade, Test.Name, Test_result.date_time).filter(
                Test_result.user.has(id=current_user.id), Test_result.test.has(id=2), Test.id == 2).order_by(
                Test_result.date_time.desc()).limit(1)
            testdata11c = db.session.query(Test_result.grade, Test.Name, Test_result.date_time).filter(
                Test_result.user.has(id=current_user.id), Test_result.test.has(id=3), Test.id == 3).order_by(
                Test_result.date_time.desc()).limit(1)
            user_ra9c = db.session.query(User_answers).filter(
                User_answers.user_id == current_user.id,
                User_answers.task.has(test_id=1)
            ).all()
            user_ra10c = db.session.query(User_answers).filter(
                User_answers.user_id == current_user.id,
                User_answers.task.has(test_id=2)
            ).all()
            user_ra11c = db.session.query(User_answers).filter(
                User_answers.user_id == current_user.id,
                User_answers.task.has(test_id=3)
            ).all()
    return render_template('profile.html', user=user, testdata9c=testdata9c, testdata10c=testdata10c,
                           testdata11c=testdata11c, title="Личный кабинет", menu=user_menu,
                           user_ra9c=user_ra9c, user_ra10c=user_ra10c, user_ra11c=user_ra11c, footer=True)


# @app.route('/print_certificate')
# def print_certificate():
#     # Путь к изображению сертификата
#     certificate_path = os.path.join(UPLOAD_FOLDER, 'certificate.png')
#
#     # Создаем временный файл для сохранения PDF
#     temp_pdf_file = tempfile.NamedTemporaryFile(delete=False)
#     pdf_output_path = temp_pdf_file.name
#
#     # Инициализируем PDF документ с поддержкой русских символов
#     pdf = FPDF(orientation='P', unit='mm', format='A4')
#     pdf.add_page()
#     pdf.add_font('DejaVuSans', '', FONT_PATH, uni=True)  # Используем DejaVuSans
#
#     # Загружаем изображение с помощью PIL
#     certificate_image = PILImage.open(certificate_path)
#
#     # Подгоняем размер изображения под размер страницы PDF
#     pdf_width = 210  # Ширина страницы в мм (A4)
#     pdf_height = 297  # Высота страницы в мм (A4)
#     img_width, img_height = certificate_image.size
#     aspect_ratio = img_width / img_height
#     if img_width > pdf_width or img_height > pdf_height:
#         if aspect_ratio > 1:
#             img_width = pdf_width
#             img_height = img_width / aspect_ratio
#         else:
#             img_height = pdf_height
#             img_width = img_height * aspect_ratio
#
#     # Вставляем изображение на страницу PDF
#     pdf.image(certificate_path, x=(pdf_width - img_width) / 2, y=(pdf_height - img_height) / 2, w=img_width,
#               h=img_height)
#
#     # Добавляем личные данные пользователя
#     user = UserPersonalInfo.query.filter(UserPersonalInfo.user_id == current_user.id).first()
#     test = Test.query.filter(Test.id == 1).first()
#     test_res_info = Test_result.query.filter(Test_result.test_id == 1, Test_result.user_id == current_user.id).first()
#     print(test_res_info)
#     user_info = f"Награждается\n{user.surname} {user.name} {user.patronymic}\nученик школы №{user.school}\nучащийся {user.s_class} класса\nза прохождение теста {test.Name}\n" \
#                 f"набравший {test_res_info.grade} баллов"
#
#     pdf.set_text_color(0, 0, 0)
#
#     # Устанавливаем координаты расположения текста
#     text_x = 12  # Координата X
#     text_y = 100  # Координата Y
#     pdf.set_xy(text_x, text_y)
#
#     # Добавляем текст с использованием DejaVuSans шрифта
#     pdf.set_font('DejaVuSans', '', 18)
#     pdf.multi_cell(0, 12, user_info, align='C')
#
#     # Сохраняем PDF документ
#     pdf.output(pdf_output_path)
#
#     # Закрываем временный файл
#     temp_pdf_file.close()
#
#     # Отправляем файл клиенту для скачивания
#     return send_file(pdf_output_path, as_attachment=True, download_name='certificate.pdf', mimetype='application/pdf')


@app.route('/test9c', methods=["GET", "POST"])
def test_9c():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    elif current_user.is_authenticated:
        cur_u = User.query.filter(User.id == current_user.id).first()
        if cur_u.usertype == "Администратор":
            return render_template("index.html", menu=admin_menu, footer=True)
        else:
            pd = db.session.query(UserPersonalInfo).filter(UserPersonalInfo.user_id == current_user.id).first()
            if not pd:
                return redirect(url_for('pd'))
            else:
                test = Test.query.get(1)
                tasks = test.tasks

                test_result = Test_result.query.filter_by(user_id=current_user.id, test_id=1).first()

                if request.method == "POST":
                    grade = 0

                    for i, task in enumerate(tasks, start=1):
                        form_answer = request.form[f"answer{i}"].replace('.', ',', 1).strip()
                        tr_ra_res = User_answers(user_id=current_user.id, task_id=i, answer=form_answer)
                        correct_answer = task.Answer
                        if form_answer == correct_answer:
                            grade += 1
                            tr_ra_res.is_answer_correct = True
                        else:
                            tr_ra_res.is_answer_correct = False
                        db.session.add(tr_ra_res)
                        db.session.commit()
                    time = datetime.now()
                    res = Test_result(test_id=1, user_id=current_user.id, grade=grade, date_time=time)
                    db.session.add(res)
                    db.session.commit()

                    return redirect(
                        url_for('profile', id=current_user.id, title="Личный кабинет", menu=user_menu, footer=True))

    if not test_result:
        return render_template("test.html", test=test, tasks=tasks, title="Тестирование", menu=user_menu, footer=True)
    else:
        return redirect(url_for('profile', id=current_user.id))


@app.route('/test10c', methods=["GET", "POST"])
def test_10c():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    elif current_user.is_authenticated:
        cur_u = User.query.filter(User.id == current_user.id).first()
        if cur_u.usertype == "Администратор":
            return render_template("index.html", menu=admin_menu, footer=True)
        else:
            pd = db.session.query(UserPersonalInfo).filter(UserPersonalInfo.user_id == current_user.id).first()
            if not pd:
                return redirect(url_for('pd'))
            else:
                test = Test.query.get(2)
                tasks = test.tasks

                test_result = Test_result.query.filter_by(user_id=current_user.id, test_id=2).first()

                if request.method == "POST":
                    grade = 0

                    for i, task in enumerate(tasks, start=1):
                        form_answer = request.form[f"answer{i}"].replace('.', ',', 1).strip()
                        tr_ra_res = User_answers(user_id=current_user.id, task_id=i + 7, answer=form_answer)
                        correct_answer = task.Answer
                        if form_answer == correct_answer:
                            grade += 1
                            tr_ra_res.is_answer_correct = True
                        else:
                            tr_ra_res.is_answer_correct = False
                        db.session.add(tr_ra_res)
                        db.session.commit()
                    time = datetime.now()
                    res = Test_result(test_id=2, user_id=current_user.id, grade=grade, date_time=time)
                    db.session.add(res)
                    db.session.commit()

                    return redirect(
                        url_for('profile', id=current_user.id, title="Личный кабинет", menu=user_menu, footer=True))

    if not test_result:
        return render_template("test.html", test=test, tasks=tasks, title="Тестирование", menu=user_menu, footer=True)
    else:
        return redirect(url_for('profile', id=current_user.id))


@app.route('/test11c', methods=["GET", "POST"])
def test_11c():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    elif current_user.is_authenticated:
        cur_u = User.query.filter(User.id == current_user.id).first()
        if cur_u.usertype == "Администратор":
            return render_template("index.html", menu=admin_menu, footer=True)
        else:
            pd = db.session.query(UserPersonalInfo).filter(UserPersonalInfo.user_id == current_user.id).first()
            if not pd:
                return redirect(url_for('pd'))
            else:
                test = Test.query.get(3)
                tasks = test.tasks

                test_result = Test_result.query.filter_by(user_id=current_user.id, test_id=3).first()

                if request.method == "POST":
                    grade = 0

                    for i, task in enumerate(tasks, start=1):
                        form_answer = request.form[f"answer{i}"].replace('.', ',', 5).strip()
                        tr_ra_res = User_answers(user_id=current_user.id, task_id=i + 14, answer=form_answer)
                        correct_answer = task.Answer
                        if form_answer == correct_answer:
                            grade += 1
                            tr_ra_res.is_answer_correct = True
                        else:
                            tr_ra_res.is_answer_correct = False
                        db.session.add(tr_ra_res)
                        db.session.commit()
                    time = datetime.now()
                    res = Test_result(test_id=3, user_id=current_user.id, grade=grade, date_time=time)
                    db.session.add(res)
                    db.session.commit()

                    return redirect(
                        url_for('profile', id=current_user.id, title="Личный кабинет", menu=user_menu, footer=True))

    if not test_result:
        return render_template("test.html", test=test, tasks=tasks, title="Тестирование", menu=user_menu, footer=True)
    else:
        return redirect(url_for('profile', id=current_user.id))


@app.route('/MUList', methods=['GET', 'POST'])
def list_MU():
    if current_user.is_authenticated:
        cur_u = User.query.filter(User.id == current_user.id).first()
        if cur_u.usertype == "Администратор":
            return render_template("index.html", menu=admin_menu, footer=True)

    tasks = MUList.query.all()
    years = set(task.publication_year for task in tasks)
    years = sorted(years, reverse=True)
    classes = set(task.teach_class for task in tasks)
    classes = sorted(classes, reverse=True)

    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(MUList.title, MUList.publication_year, MUList.teach_class, MUList.pdf_file).paginate(
        page=page, per_page=5)
    selected_year = request.args.get('year')
    if selected_year:
        pagination = db.session.query(MUList.title, MUList.publication_year, MUList.pdf_file,
                                      MUList.teach_class).filter_by(
            publication_year=selected_year).paginate(
            page=page, per_page=5)
    selected_class = request.args.get('class')
    if selected_class:
        pagination = db.session.query(MUList.title, MUList.publication_year, MUList.pdf_file,
                                      MUList.teach_class).filter_by(
            teach_class=selected_class).paginate(
            page=page, per_page=5)
    if selected_class and selected_year:
        pagination = db.session.query(MUList.title, MUList.publication_year, MUList.pdf_file,
                                      MUList.teach_class).filter_by(
            teach_class=selected_class, publication_year=selected_year).paginate(
            page=page, per_page=5)

    return render_template('files.html', years=years, classes=classes, menu=user_menu, selected_year=selected_year,
                           selected_class=selected_class,
                           pagination=pagination, header="Методические указания", title="Методические указания",
                           footer=True)


@app.route('/task_archive', methods=['GET', 'POST'])
def list_tasks():
    if current_user.is_authenticated:
        cur_u = User.query.filter(User.id == current_user.id).first()
        if cur_u.usertype == "Администратор":
            return render_template("index.html", menu=admin_menu, footer=True)

    tasks = TaskArchive.query.all()

    years = set(task.publication_year for task in tasks)
    years = sorted(years, reverse=True)
    classes = set(task.teach_class for task in tasks)
    classes = sorted(classes, reverse=True)

    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(TaskArchive.title, TaskArchive.publication_year, TaskArchive.teach_class,
                                  TaskArchive.pdf_file).paginate(
        page=page, per_page=5)
    selected_year = request.args.get('year')
    if selected_year:
        pagination = db.session.query(TaskArchive.title, TaskArchive.publication_year, TaskArchive.pdf_file,
                                      TaskArchive.teach_class).filter_by(
            publication_year=selected_year).paginate(
            page=page, per_page=5)
    selected_class = request.args.get('class')
    if selected_class:
        pagination = db.session.query(TaskArchive.title, TaskArchive.publication_year, TaskArchive.pdf_file,
                                      TaskArchive.teach_class).filter_by(
            teach_class=selected_class).paginate(
            page=page, per_page=5)
    if selected_class and selected_year:
        pagination = db.session.query(TaskArchive.title, TaskArchive.publication_year, TaskArchive.pdf_file,
                                      TaskArchive.teach_class).filter_by(
            teach_class=selected_class, publication_year=selected_year).paginate(
            page=page, per_page=5)

    return render_template('files.html', years=years, classes=classes, menu=user_menu, selected_year=selected_year,
                           selected_class=selected_class,
                           pagination=pagination, header="Методические указания", title="Методические указания",
                           footer=True)


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    file_path = os.path.join(app.config['DOWNLOAD_FOLDER_ARCHIVE'], filename)
    return send_file(file_path, as_attachment=True)


@app.route('/admin/test_result')
def test_result():
    if current_user.is_authenticated:
        cur_u = User.query.filter(User.id == current_user.id).first()
        if cur_u.usertype == "Администратор":
            return render_template("index.html", menu=admin_menu, footer=True)

            page = request.args.get('page', 1, type=int)
            pagination = db.session.query(UserPersonalInfo, Test, Test_result).filter(
                UserPersonalInfo.user_id == User.id).filter(
                Test_result.user_id == User.id).filter(Test_result.test_id == Test.id).paginate(
                page=page, per_page=5)
            return render_template('test_result.html', pagination=pagination, title="Просмотр результатов",
                                   menu=admin_menu)
        else:
            return render_template('index.html', menu=user_menu, title='Главная страница')


@app.route('/admin/edit/9c', methods=["GET", "POST"])
def edit_test():
    if current_user.is_authenticated:
        cur_u = User.query.filter(User.id == current_user.id).first()
        if cur_u.usertype == "Администратор":
            form = editTest(request.form, crsf_enabled=False)
            if request.method == 'POST' and form.validate_on_submit():
                test = Test.query.filter_by(id=1).first()
                questions = [f'quest{i}' for i in range(1, 8)]
                answers = [f'answ{i}' for i in range(1, 8)]
                pictures = [f'pic{i}' for i in range(1, 8)]
                tasks = TestTask.query.filter(TestTask.test_id == test.id).all()
                for i in range(7):
                    task = tasks[i]
                    task.Question = form.data[questions[i]]
                    task.Answer = form.data[answers[i]].strip()
                    if pictures[i] in request.files and request.files[pictures[i]].filename:
                        file = request.files[pictures[i]]
                        if file.filename.split(".")[-1] in ALLOWED_EXTENSIONS and "image" in file.mimetype:
                            filename = secure_filename(file.filename)
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            task.picture = filename
                db.session.commit()
            if not form.validate_on_submit():
                print(form.errors)
        else:
            return render_template('index.html', menu=user_menu, title='Главная страница')
    return render_template("edit_test.html", FlaskForm=form, menu=admin_menu)


@app.route('/admin/edit/10c', methods=["GET", "POST"])
def edit_test_10c():
    if current_user.is_authenticated:
        cur_u = User.query.filter(User.id == current_user.id).first()
        if cur_u.usertype == "Администратор":
            form = editTest(request.form, crsf_enabled=False)
            if request.method == 'POST' and form.validate_on_submit():
                test = Test.query.filter_by(id=2).first()
                questions = [f'quest{i}' for i in range(1, 8)]
                answers = [f'answ{i}' for i in range(1, 8)]
                pictures = [f'pic{i}' for i in range(1, 8)]
                tasks = TestTask.query.filter(TestTask.test_id == test.id).all()
                for i in range(7):
                    task = tasks[i]
                    task.Question = form.data[questions[i]]
                    task.Answer = form.data[answers[i]].strip()
                    if pictures[i] in request.files and request.files[pictures[i]].filename:
                        file = request.files[pictures[i]]
                        if file.filename.split(".")[-1] in ALLOWED_EXTENSIONS and "image" in file.mimetype:
                            filename = secure_filename(file.filename)
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            task.picture = filename
                db.session.commit()
            if not form.validate_on_submit():
                print(form.errors)
        else:
            return render_template('index.html', menu=user_menu, title='Главная страница')
    return render_template("edit_test.html", FlaskForm=form, menu=admin_menu)


@app.route('/admin/edit/11c', methods=["GET", "POST"])
def edit_test_11c():
    if current_user.is_authenticated:
        cur_u = User.query.filter(User.id == current_user.id).first()
        if cur_u.usertype == "Администратор":
            form = editTest(request.form, crsf_enabled=False)
            if request.method == 'POST' and form.validate_on_submit():
                test = Test.query.filter_by(id=3).first()
                questions = [f'quest{i}' for i in range(1, 8)]
                answers = [f'answ{i}' for i in range(1, 8)]
                pictures = [f'pic{i}' for i in range(1, 8)]
                tasks = TestTask.query.filter(TestTask.test_id == test.id).all()
                for i in range(7):
                    task = tasks[i]
                    task.Question = form.data[questions[i]]
                    task.Answer = form.data[answers[i]].strip()
                    if pictures[i] in request.files and request.files[pictures[i]].filename:
                        file = request.files[pictures[i]]
                        if file.filename.split(".")[-1] in ALLOWED_EXTENSIONS and "image" in file.mimetype:
                            filename = secure_filename(file.filename)
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            task.picture = filename
                db.session.commit()
            if not form.validate_on_submit():
                print(form.errors)
        else:
            return render_template('index.html', menu=user_menu, title='Главная страница')
    return render_template("edit_test.html", FlaskForm=form, menu=admin_menu)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/admin/upload_MU', methods=['GET', 'POST'])
def upload_file_MU():
    if current_user.is_authenticated:
        cur_u = User.query.filter(User.id == current_user.id).first()
        if cur_u.usertype == "Администратор":
            if request.method == 'POST':
                file = request.files['pdf_file']
                task_name = request.form['task_name']
                teach_class = request.form['class']

                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER_ARCHIVE'], filename)
                    file.save(file_path)

                    current_year = datetime.now().year

                    new_task = MUList(title=task_name, pdf_file=filename, publication_year=current_year,
                                      teach_class=teach_class)
                    db.session.add(new_task)
                    db.session.commit()

                    return redirect(url_for('index'))
        else:
            return render_template('index.html', menu=user_menu, title='Главная страница')
    return render_template('upload.html', menu=admin_menu)


@app.route('/admin/upload_archive', methods=['GET', 'POST'])
def upload_file_archive():
    if current_user.is_authenticated:
        cur_u = User.query.filter(User.id == current_user.id).first()
        if cur_u.usertype == "Администратор":
            if request.method == 'POST':
                file = request.files['pdf_file']
                task_name = request.form['task_name']
                teach_class = request.form['class']

                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER_ARCHIVE'], filename)
                    file.save(file_path)

                    current_year = datetime.now().year

                    new_task = TaskArchive(title=task_name, pdf_file=filename, publication_year=current_year,
                                           teach_class=teach_class)
                    db.session.add(new_task)
                    db.session.commit()

                    return redirect(url_for('list_tasks'))
            else:
                return render_template('index.html', menu=user_menu, title='Главная страница')
    return render_template('upload.html', menu=admin_menu)
