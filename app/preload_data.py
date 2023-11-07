from werkzeug.security import generate_password_hash

from app import db, app
from app.models import User, TestTask, Test


def preload_data():
    with app.app_context():
        u = User(login='OkhlupinaOV', password=generate_password_hash('1@s{zfK2'), usertype="Администратор")
        db.session.add(u)
        u = User(login='adminacc', password=generate_password_hash('@ezAkm1_{'), usertype="Администратор")
        db.session.add(u)
        u = User(login='KamozinaOV', password=generate_password_hash('@_Zkif3}z'), usertype="Администратор")
        db.session.add(u)
        db.session.commit()
        print("Успешно добавлены 3 администратора\n")
        new_test = Test(Name="9 класс")
        db.session.add(new_test)

        new_task = TestTask(
            Question=f"Задание №1",
            Answer=f"45",
            picture="9_1.png",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Задание №2",
            Answer=f"3",
            picture="9_2.png",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Задание №3",
            Answer=f"2",
            picture="9_3.png",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Задание №4",
            Answer=f"30",
            picture="9_4.png",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Задание №5",
            Answer=f"22",
            picture="9_5.png",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Задание №6",
            Answer=f"60",
            picture="9_6.png",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Задание №7",
            Answer=f"68",
            picture="9_7.png",
            test=new_test)

        db.session.add(new_task)

        db.session.commit()

        print("Добавлен тест 9-ого класса и 7 вопросов")

        new_test = Test(Name="10 класс")
        db.session.add(new_test)

        new_task = TestTask(
            Question=f"Задание №1",
            Answer=f"106",
            picture="10_1.png",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Задание №2",
            Answer=f"8",
            picture="10_2.png",
            test=new_test)

        db.session.add(new_task)


        new_task = TestTask(
            Question=f"Задание №3",
            Answer=f"понедельник",
            picture="10_3.png",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Задание №4",
            Answer=f"20",
            picture="10_4.png",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Задание №5",
            picture="10_5.png",
            Answer=f"40",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Задание №6",
            picture="10_6.png",
            Answer=f"60",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Задание №7",
            picture="10_7.png",
            Answer=f"5",
            test=new_test)

        db.session.add(new_task)

        db.session.commit()

        print("Добавлен тест 10-ого класса и 7 вопросов")

        new_test = Test(Name="11 класс")
        db.session.add(new_test)

        new_task = TestTask(
            Question=f"Задание №1",
            picture="11_1.png",
            Answer=f"1,6",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Задание №2",
            picture="11_2.png",
            Answer=f"8",
            test=new_test)

        db.session.add(new_task)


        new_task = TestTask(
            Question=f"Задание №3",
            picture="11_3.png",
            Answer=f"3",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Задание №4",
            picture="11_4.png",
            Answer=f"765",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Задание №5",
            picture="11_5.png",
            Answer=f"5",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Задание №6",
            picture="11_6.png",
            Answer=f"5",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Задание №7",
            picture="11_7.png",
            Answer=f"-3,5",
            test=new_test)

        db.session.add(new_task)

        db.session.commit()

        print("Добавлен тест 11-ого класса и 7 вопросов")

        db.session.commit()
        print("Успешно добавлены 3 теста\n")


preload_data()
