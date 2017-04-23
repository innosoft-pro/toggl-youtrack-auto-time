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

start_date, end_date - даты, начиная и заканчивая которыми нужно загружать/форматировать данные из тоггла
поддерживаются следующие варианты: today, yesterday, tomorrow, "%d-%m-%Y". 
Трекание всегда происходит за сутки, время - utc. (т.е. если вносить данные за сегодняшний день, 
внесутся данные с 03:00 сегодня до 03:00 завтра по мск)

Для start_date дефолтный параметр - today, для end_date - tomorrow.

Таким образом, команда

    python3 toggl_youtrack.py --track --format yesterday today

внесет данные за вчерашний день в ютрек и отформатирует эти записи

команда

    python3 toggl_youtrack.py --track --format today

внесет данные за сегодняшний день в ютрек и отформатирует эти записи

команда

    python3 toggl_youtrack.py --track --format yesterday

или

    python3 toggl_youtrack.py --track --format yesterday tomorrow


внесет данные за вчерашний и сегодняшний день в ютрек и отформатирует эти записи


команда

    python3 toggl_youtrack.py --track --format "01-01-2017" "03-03-2017"

внесет данные за c 1 января по 3 марта в ютрек и отформатирует эти записи. 
Attention! У тоггла лимит на загрузку 9000 записей, так что лучше не переусердствовать с такими командами

# Что и как скрипт сейчас расставляет в тоггле по команде --format
1. загружает данные о subsystem из ютрека и переносит это в теги тоггла
2. загружает название таски из ютрека и переносит в тоггл
3. заполняет проект в тоггле следующим образом: если ты - ревьюер для таски в ютреке, заполняется проект Quality Management, 
иначе - по первому тегу таски в ютреке