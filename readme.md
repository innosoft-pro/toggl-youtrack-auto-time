# Что это?
Это скрипт, который умеет делать две простых вещи:
1. переносить данные из тоггла в ютрек за определенный интервал дат по id таски в ютреке
2. расставлять в тоггле проекты и теги по данным из ютрека

Attention!
скрипт тупой и не запоминает, что он вносил раньше, поэтому не рекомендуется запускать его на одних и тех же данных несколько раз

# Перед первым использованием
1. установи requirements

 
    sudo pip3 install -r requirements.txt


2. Создай конфиг в корне под любым именем (дефолтное - config.json).


    {
      "toggl": {
        "login": "name@example.com",
        "password": "top_secret_password",
        "workspace": "workspace_name"
      },
      "youtrack": {
        "link": "https://youtrack.example.com",
        "login": "name",
        "password": "top_secret_password",
        "tasks_prefix": "MMX"
      }
    }

Если нужно подгрузить конфиг не с дефолтным именем, то используй 
переменную среды CFG:

    CFG=my_config.json python3 toggl_youtrack.py --track --format

Attention! Логины и пароли хранятся в plain text, но кого это волнует.

# Как пользоваться?

    python3 toggl_youtrack.py --track --format <start_date> <end_date>
    
--track - выставь, если хочешь перенести данные из тоггла в ютрек

--format - выставь, если хочешь расставить в тоггле проекты и теги по данным из ютрека

--since_last - выставь, если ты уже пользовался скриптом раньше и хочешь затрекать время с учетом твоего 
предыдущего запуска скрипта. Подробнее см. "Опция --since_last"

--starting_from - выставь, если хочешь задать отличный от `today` параметр начала загрузки треков из тоггла

--until - выставь, если хочешь задать отличный от `tomorrow` параметр начала загрузки треков из тоггла

starting_from, until - даты, начиная и заканчивая которыми нужно загружать/форматировать данные из тоггла
поддерживаются следующие варианты: today, yesterday, tomorrow, "%d-%m-%Y", "%d-%m-%Y %H:%M:%S". 
Время всегда используется utc. (т.е. если вносить данные за сегодняшний день, 
внесутся данные с 03:00 сегодня до 03:00 завтра по мск)

Для starting_from дефолтный параметр - today, для until - tomorrow.

Таким образом, команда

    python3 toggl_youtrack.py --track --format --starting_from=yesterday --until=today

внесет данные за вчерашний день в ютрек и отформатирует эти записи

команда

    python3 toggl_youtrack.py --track --format --starting_from=today

внесет данные за сегодняшний день в ютрек и отформатирует эти записи

команда

    python3 toggl_youtrack.py --track --format --starting_from=yesterday

или

    python3 toggl_youtrack.py --track --format --starting_from=yesterday --until=tomorrow


внесет данные за вчерашний и сегодняшний день в ютрек и отформатирует эти записи


команда

    python3 toggl_youtrack.py --track --format --starting_from='01-01-2017 12:00:00' --until=03-03-2017

внесет данные за c 12:00(UTC) 1 января по 00:00 3 марта в ютрек и отформатирует эти записи. 

Attention! У тоггла лимит на загрузку 9000 записей, так что лучше не переусердствовать с такими командами

# Что и как скрипт сейчас расставляет в тоггле по команде --format
1. загружает данные о subsystem из ютрека и переносит это в теги тоггла
2. загружает название таски из ютрека и переносит в тоггл
3. заполняет проект в тоггле следующим образом: если ты - ревьюер для таски в ютреке, заполняется проект Quality Management, 
иначе - по первому тегу таски в ютреке

# Опция --since_last
Скрипт при каждом запуске с опцией --track запоминает (данные сохраняет в файл launch_data.json в корне), 
до какого времени (параметр --until) он загружал данные в ютрек. 
Также он идентифицирует эти данные с именем конфига (т.е. для разных конфигов можно вести свою историю)

Затем, при запуске с опцией --since_last, он начнет загружать данные, начиная с этого времени и до текущего момента.
Текущий момент также будет сохранен как момент последнего запуска (если опция --track выставлена)

Пример:
Пусть сегодняшнее число - 23.04.2017 
Была использована команда:

    CFG=my_config.json python3 toggl_youtrack.py --track --format --starting_from=yesterday --until=today

Скрипт запомнил, что данные были затреканы до `23-04-2017 00:00:00`
В следующий раз была использована команда

    CFG=my_config.json python3 toggl_youtrack.py --track --format --since_last

Скрипт будет загружать данные из тоггла с `start_time=23-04-2017 00:00:00` до текущего момента 
и запомнит текущий момент. Пусть это будет `23-04-2017 14:30:00`

В следующий раз скрипт по этой же команде начнет вносить данные с `start_time=23-04-2017 14:30:00` и т.д.

Если воспользоваться опцией --since_last, не пользуясь до этого другими вариантами, скрипт выдаст ошибку, 
т.к. нет предыдущих сохраненных данных
