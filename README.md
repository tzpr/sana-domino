# sana-domino

Python ohjelmointia aloittelijoille ([A930011](https://courses.helsinki.fi/fi/a930011/117989156)) -kurssin harjoitustyö.

Ohjelma pelaa sana-dominoa kanssasi annetun sanalistan avulla.

### Alkutoimet

Koneelle asennettuna mielellään [python 3](https://www.python.org/downloads/)

Kloonaa repo

Mene sana-domino -hakemistoon

Alusta virtuaaliympäristö ohjelman käyttöön (ei pakollista mutta kätevää koska ei sotke muuta ympäristöä):
```
python3 -m venv sana-domino-env
```
Aktivoi ympäristö:
```
. sana-domino-env/bin/activate
```
Asenna tarvittavat moduulit (vain yksi [func_timeout](https://pypi.python.org/pypi/func_timeout/4.2.0))
```
pip install func_timeout
```
Valmis.


### Käyttö ja pelaaminen
```
Usage: python domino.py [options]

Options:
  -h, --help            show this help message and exit
  -l DIFFICULTY_LEVEL, --level=DIFFICULTY_LEVEL
                        Difficulty level for computer (1-10)
  -t TIMER, --timer=TIMER
                        Timeout for one move
  -p PLAYER_COUNT, --players=PLAYER_COUNT
                        Number of computer players
  -r TOURNAMENT_ROUNDS, --rounds=TOURNAMENT_ROUNDS
                        Tournament mode. Give number of rounds.
```

### Aihetta sivuavia linkkejä
- https://pypi.python.org/pypi/func_timeout/4.2.0
- https://docs.python.org/3/tutorial/errors.html
- https://www.thecodeship.com/patterns/guide-to-python-function-decorators/
- http://www.dreamsyssoft.com/python-scripting-tutorial/optionparser-tutorial.php
- https://docs.python.org/3/tutorial/controlflow.html
- https://docs.python.org/3/faq/programming.html#why-am-i-getting-an-unboundlocalerror-when-the-variable-has-a-value
