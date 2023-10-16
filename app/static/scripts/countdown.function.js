;(function () {
    'use strict';

    // значение времени на момент запуска скрипта
    const now = new Date();
    // объекты, в которые будем выводить показания таймера
    const hBox = document.getElementById('hour'),
        mBox = document.getElementById('minutes'),
        sBox = document.getElementById('seconds');

    // массив данных в котором находятся значения оставшихся до
    // конца суток часов, минут и секунд соответственно, которые
    // мы получаем путём вычитания из их максимального значения текущего
    let times = [
        now.setHours = 1,
        now.setMinutes = 30,
        now.setSeconds = 1,
    ];

    const timer = times => {
        // объявляем идентификатор таймера и запускаем функцию 'setInterval'
        let tm = setInterval(() => {
            // уменьшаем значение секунд на 1
            times[2]--;

            // проверяем, не обнулился ли таймер и если да, то останавливаем 'setInterval'
            if (times[0] == 0 && times[1] == 0 && times[2] == 0) {
                clearInterval(tm);
            } else if (times[2] == -1) {
                // если секунды имеют отрицательное значение, это значит, что
                // они перешли 0 и должен начаться отсчёт новой минуты,
                // при этом секунды становятся равными своему максимальному значению - 59,
                // а минуты уменьшаются на 1
                times[2] = 59;
                times[1]--;
            } else if (times[1] == -1) {
                // аналогично, как для минут и секунд
                // минуты выставляем в значение 59, а час уменьшаем на 1
                times[1] = 59;
                times[0]--;
            }

            // если показания или часов, или минут, или секунд меньше 10,
            // ставим перед показанием ноль
            let h = (times[0] < 10) ? '0' + times[0] : times[0],
                m = (times[1] < 10) ? '0' + times[1] : times[1],
                s = (times[2] < 10) ? '0' + times[2] : times[2];

            // выводим значение таймера на экран
            showTimer(h, m, s);
        }, 1000);
    }

    const showTimer = (hour, min, sec) => {
        hBox.innerHTML = hour;
        mBox.innerHTML = min;
        sBox.innerHTML = sec;
    }

    timer(times);

})();
