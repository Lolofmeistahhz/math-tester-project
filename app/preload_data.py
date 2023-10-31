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
        print("Успешно добавлены 2 администратора\n")
        new_test = Test(Name="9 класс")
        db.session.add(new_test)

        new_task = TestTask(
            Question=f"График функции y=f(x) симметричен относительно прямой x=5 и уравнение f(x)=0 имеет девять различных действительных корней. Чему равна сумма всех этих корней?",
            Answer=f"45",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Известно, что a>1,b>1. Какая из следующих дробей является наибольшей? (В ответе укажите номер варианта ответа без скобки)",
            Answer=f"3",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Карина ехала от дома до парка сначала на маршрутном такси, затем на метро. Причём время движения на маршрутном такси равно времени движения на метро (временем перехода от маршрутного такси до метро пренебрегаем). В случае движения от дома до парка только на маршрутном такси, время движения оказалось бы в 1,5 раза больше затраченного Кариной. Во сколько раз время движения от дома до парка на метро оказалось бы больше времени движения на маршрутном такси?",
            Answer=f"2",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Среднее арифметическое двух положительных чисел на 75% больше меньшего из этих чисел. На сколько процентов оно меньше большего из этих чисел?",
            Answer=f"30",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Из тройки неповторяющихся цифр составили все возможные различные трёхзначные числа. Сумма этих чисел составила 4884. Определить взятые цифры.(В ответе указать сумму взятых цифр)",
            Answer=f"22",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Дан треугольник ABC. Из вершины B проведена биссектриса BD. BD=8√7, AB=21,  DC=8. Определить периметр треугольника ABC.",
            Answer=f"60",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Пусть a и b – корни квадратного уравнения x^2+x-9=0. Чему равно значение выражения 3a^2+4b^2+3a+4b+5?",
            Answer=f"68",
            test=new_test)

        db.session.add(new_task)

        db.session.commit()

        print("Добавлен тест 9-ого класса и 7 вопросов")

        new_test = Test(Name="10 класс")
        db.session.add(new_test)

        new_task = TestTask(
            Question=f"Целые неотрицательные числа k, l, m, n удовлетворяют равенству km+lm+mn=505. Найдите наименьшее значение выражения k+l+m+n.",
            Answer=f"106",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"На сколько областей делит координатную плоскость три линии: график функцииy=|x|, парабола y=5-x² и прямая x=1?",
            Answer=f"8",
            test=new_test)

        db.session.add(new_task)


        new_task = TestTask(
            Question=f"Грише 16 лет. В 2023 году он отмечал свой День рождения в воскресенье. Укажите день недели, когда родился Гриша.(Ответ записать в строчном регистре)",
            Answer=f"понедельник",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Дан прямоугольник размера 14×6. Определите площадь закрашенной на рисунке части прямоугольника.",
            Answer=f"20",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Пока Андрей делает 3 приседания, Боря успевает сделать уже 4, а пока Боря делает 5 приседаний, Витя делает 7. Общее количество приседаний, сделанных Андреем и Витей за определенное время, равно 86. Сколько приседаний за это время сделал Боря?",
            Answer=f"40",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Числитель дроби увеличили на 20%. На сколько процентов надо уменьшить знаменатель, чтобы полученная дробь была в 3 раза больше исходной?",
            Answer=f"60",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Уравнения x²+(4a-1)x+a²+3=0 и x³+(4a-1), x²+(a²+3)x+a²-1=0 имеют общие действительные корни. Найти сумму этих корней.",
            Answer=f"5",
            test=new_test)

        db.session.add(new_task)

        db.session.commit()

        print("Добавлен тест 10-ого класса и 7 вопросов")

        new_test = Test(Name="11 класс")
        db.session.add(new_test)

        new_task = TestTask(
            Question=f"Вычислить",
            Answer=f"1,6",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Определите значение выражения √(36-t^2 )+√(20-t^2 ) (без нахождения переменной), зная, что разность корней √(36-t^2 )и √(20-t^2 )принимает значение, равное 2.",
            Answer=f"8",
            test=new_test)

        db.session.add(new_task)


        new_task = TestTask(
            Question=f"Вычислить значение A², если A=tg20° + 4sin20°.",
            Answer=f"3",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Дана возрастающая арифметическая прогрессия, у которой a_1+a_2+a_3=21. Если a_1-1=b_1, a_2-1=b_2, a_3+2=b_3, то b_1,b_2,b_3 образуют геометрическую прогрессию. Вычислить сумму первых её восьми членов.",
            Answer=f"765",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Решить уравнение.",
            Answer=f"5",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Треугольник ABC имеет площадь 25 см². Точка D делит сторону AC в отношении 2:3. DE⊥BC, DE=6см. Чему равна длина стороны BC?",
            Answer=f"5",
            test=new_test)

        db.session.add(new_task)

        new_task = TestTask(
            Question=f"Решите неравенство f'(x)+g'(x)≤0, при условии что f(x)=2x³+12x², f(x)=9x²+72x. В ответе укажите середину отрезка решения.",
            Answer=f"-3,5",
            test=new_test)

        db.session.add(new_task)

        db.session.commit()

        print("Добавлен тест 11-ого класса и 7 вопросов")

        db.session.commit()
        print("Успешно добавлены 3 теста\n")


preload_data()
