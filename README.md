ogame-parser
============

ogame-parser is an OGame parsing tool.


Requirements
------------

ogame-parser is written in Python. Required Python packages are listed in ``pip-requirements.txt``.

Usage
-----

1. Copy ``example_local_config.py`` to ``local_config.py``
2. Edit ``local_config.py`` and insert yor own login and password.
3. Run: ``python parser.py``

Sample output:
```
ogame-parser$ python parser.py
Logging in...
Planet(name="Quakland", coords="1:194:12", planetid="33627296")
metal {'current': 65411, 'per_hour': 3032, 'capacity': 255000, 'level': 18}
crystal {'current': 34558, 'per_hour': 1078, 'capacity': 140000, 'level': 14}
deuterium {'current': 7772, 'per_hour': 306, 'capacity': 75000, 'level': 10}
Planet(name="Qavntiajchaw", coords="1:194:11", planetid="33635110")
metal {'current': 84394, 'per_hour': 1910, 'capacity': 255000, 'level': 15}
crystal {'current': 46780, 'per_hour': 1734, 'capacity': 140000, 'level': 17}
deuterium {'current': 25728, 'per_hour': 303, 'capacity': 75000, 'level': 9}
Planet(name="Ranaduniyartamu", coords="1:194:7", planetid="33648315")
metal {'current': 43811, 'per_hour': 667, 'capacity': 75000, 'level': 9}
crystal {'current': 34766, 'per_hour': 1268, 'capacity': 75000, 'level': 15}
deuterium {'current': 5771, 'per_hour': 380, 'capacity': 20000, 'level': 11}
Planet(name="Meeraharah", coords="1:194:5", planetid="33653920")
metal {'current': 59523, 'per_hour': 1625, 'capacity': 75000, 'level': 14}
crystal {'current': 35252, 'per_hour': 1485, 'capacity': 75000, 'level': 16}
deuterium {'current': 4268, 'per_hour': 13, 'capacity': 10000, 'level': 1}
```


