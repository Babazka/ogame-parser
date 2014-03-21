ogame-parser
============

Парсит страницы игры OGame и выводит сводку по ресурсам и флотам на ваших планетах.

Работает только с русской локализацией игры.


Requirements
------------

ogame-parser написан на языке Python (2.7). Список зависимостей перечислен в ``pip-requirements.txt``.

Использование
-------------

1. Скопировать ``example_local_config.py`` в ``local_config.py``
2. Отредактировать ``local_config.py``, вставив свой логин, пароль и игровой сервер.
3. Создать пустой файл ``first_screen.html``
4. Запустить: ``python parser.py``

Пример вывода:
```
ogame-parser$ python parser.py
Logging in...
Planet(name="Quakland", coords="1:194:12", planetid="33627296")
        metal           current   50616 per_hour           3032 capacity         255000 level        18 next lvl          88673 mt   22168 cr   need      38057 mt    8337 cr     109 dE
        crystal         current   13831 per_hour           1078 capacity         140000 level        14 next lvl          34587 mt   17293 cr   need          0 mt    3462 cr      42 dE
        deuterium       current    8678 per_hour            306 capacity          75000 level        10 next lvl          12974 mt    4324 cr   need          0 mt       0 cr      56 dE
        energy          current      53 per_hour              0 capacity              0 level        18 next lvl         110841 mt   44336 cr   need      60225 mt   30505 cr       0 dE
        Лёгкий истребитель: 5   Тяжёлый истребитель: 2  Крейсер: 1
        Малый транспорт: 6      Большой транспорт: 5    Ёмкость: 155000

Planet(name="Qavntiajchaw", coords="1:194:11", planetid="33635110")
        metal           current   73391 per_hour           1910 capacity         255000 level        15 next lvl          26273 mt    6568 cr   need          0 mt       0 cr       0 dE
        crystal         current   37643 per_hour           1734 capacity         140000 level        17 next lvl         141670 mt   70835 cr   need      68279 mt   33192 cr       0 dE
        deuterium       current   25448 per_hour            303 capacity          75000 level         9 next lvl           8649 mt    2883 cr   need          0 mt       0 cr       0 dE
        energy          current     412 per_hour              0 capacity              0 level        19 next lvl         166262 mt   66505 cr   need      92871 mt   28862 cr       0 dE
        Большой транспорт: 5    Ёмкость: 125000

Planet(name="Ranaduniyartamu", coords="1:194:7", planetid="33648315")
        metal           current   45835 per_hour            667 capacity          75000 level         9 next lvl           2306 mt     576 cr   need          0 mt       0 cr       0 dE
        crystal         current   38615 per_hour           1268 capacity          75000 level        15 next lvl          55340 mt   27670 cr   need       9505 mt       0 cr       0 dE
        deuterium       current    6932 per_hour            380 capacity          20000 level        11 next lvl          19461 mt    6487 cr   need          0 mt       0 cr       0 dE
        energy          current     250 per_hour              0 capacity              0 level        17 next lvl          73894 mt   29557 cr   need      28059 mt       0 cr       0 dE
        Тяжёлый истребитель: 2
        Малый транспорт: 1      Большой транспорт: 4    Ёмкость: 105000

Planet(name="Meeraharah", coords="1:194:5", planetid="33653920")
        metal           current   64456 per_hour           1625 capacity          75000 level        14 next lvl          17515 mt    4378 cr   need          0 mt       0 cr       0 dE
        crystal         current   39761 per_hour           1485 capacity          75000 level        16 next lvl          88544 mt   44272 cr   need      24088 mt    4511 cr       0 dE
        deuterium       current    4313 per_hour             13 capacity          10000 level         1 next lvl            337 mt     112 cr   need          0 mt       0 cr       0 dE
        energy          current     180 per_hour              0 capacity              0 level        16 next lvl          49263 mt   19705 cr   need          0 mt       0 cr       0 dE
        Малый транспорт: 1      Большой транспорт: 4    Ёмкость: 105000

TOTAL:
        metal           current  234298 per_hour           7234 per_day  173616
        crystal         current  129850 per_hour           5565 per_day  133560
        deuterium       current   45371 per_hour           1002 per_day   24048
        Лёгкий истребитель 5
        Тяжёлый истребитель 4
        Крейсер 1
        Малый транспорт 8
        Большой транспорт 18
```
