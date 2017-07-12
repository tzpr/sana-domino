# sana-domino

Python ohjelmointia aloittelijoille ([A930011](https://courses.helsinki.fi/fi/a930011/117989156)) -kurssin harjoitustyö.

Ohjelma pelaa sana-dominoa kanssasi annetun sanalistan avulla.

### Alkutoimet

Koneelle asennettuna mielellään [python 3](https://www.python.org/downloads/)

Kloonaa repo

Mene sana-domino -hakemistoon

Alusta [virtuaaliympäristö](https://docs.python.org/3/library/venv.html) ohjelman käyttöön (ei pakollista, mutta kätevää koska mahdollistaa projektikohtaisen moduulien asentelun sotkematta muuta ympäristöä):

```
python3 -m venv sana-domino-env
```
Aktivoi luotu ympäristö:

```
. sana-domino-env/bin/activate
```
Asenna tarvittavat moduulit (vain yksi, [func_timeout](https://pypi.python.org/pypi/func_timeout/4.2.0))

```
pip install func_timeout
```
Valmis.


Edellä kuvatun alustuksen voi tehdä myös sana-domino -hakemistossa olevalla skriptillä (activate-env.sh).
Skripti luo virtuaaliympäristön jos sitä ei ole ja asentaa tarvittavat moduulit sekä aktivoi ympäristön.

Anna skriptille suoritusoikeus:

```
chmod u+x activate-env.sh
``` 
Suorita skripti:

``` 
. activate-env.sh
```
Valmis.


### Käyttö ja pelaaminen
```
Usage: python domino2.py [options]

Options:
  -h, --help            show this help message and exit
  -l DIFFICULTY_LEVEL, --level=DIFFICULTY_LEVEL
                        set the game difficulty level for the computer player
                        from 1-10. When no level is set the computer makes no
                        mistakes.
  -t TIMER, --timer=TIMER
                        set the maximum time for the answer.
  -p PLAYER_COUNT, --players=PLAYER_COUNT
                        set the number of computer players. Note: computer
                        players continue the game till the end!
  -r TOURNAMENT_ROUNDS, --rounds=TOURNAMENT_ROUNDS
                        set the number of rounds to be played and activate the
                        tournament mode. The winner is the one who has the
                        most wins.
```

### Aihetta sivuavia linkkejä
- Python tyyliopas: https://www.python.org/dev/peps/pep-0008/
- Pylint: https://www.pylint.org/
- https://developers.google.com/edu/python/
- https://pypi.python.org/pypi/func_timeout/4.2.0
- https://docs.python.org/3/tutorial/errors.html
- https://www.thecodeship.com/patterns/guide-to-python-function-decorators/
- http://www.dreamsyssoft.com/python-scripting-tutorial/optionparser-tutorial.php
- https://docs.python.org/3/tutorial/controlflow.html
- https://docs.python.org/3/faq/programming.html#why-am-i-getting-an-unboundlocalerror-when-the-variable-has-a-value
- http://www.dreamsyssoft.com/unix-shell-scripting/tutorial.php
- https://google.github.io/styleguide/shell.xml
- https://help.github.com/articles/basic-writing-and-formatting-syntax/
