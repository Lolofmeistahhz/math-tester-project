from werkzeug.security import generate_password_hash


from app import db, app
from app.models import User, TestTask, Test


def preload_data():
    with app.app_context():
        u = User(login='OkhlupinaOV', password=generate_password_hash('1@s{zfK2'), usertype="Администратор")
        db.session.add(u)
        u = User(login='KamozinaOV', password=generate_password_hash('@_Zkif3}z'), usertype="Администратор")
        db.session.add(u)
        db.session.commit()
        print("Успешно добавлены 2 администратора\n")
        new_test = Test(Name="9 класс")
        db.session.add(new_test)

        for i in range(1, 8):
            new_task = TestTask(
                Question=f"Вопрос {i}",
                Answer=f"Ответ {i}",
                test=new_test
            )
            db.session.add(new_task)

        db.session.commit()
        new_test = Test(Name="10 класс")
        db.session.add(new_test)

        for i in range(1, 8):
            new_task = TestTask(
                Question=f"Вопрос {i}",
                Answer=f"Ответ {i}",
                test=new_test
            )
            db.session.add(new_task)

        db.session.commit()
        new_test = Test(Name="11 класс")
        db.session.add(new_test)

        for i in range(1, 8):
            new_task = TestTask(
                Question=f"Вопрос {i}",
                Answer=f"Ответ {i}",
                test=new_test
            )
            db.session.add(new_task)

        db.session.commit()
        print("Успешно добавлены 3 теста\n")

preload_data()

