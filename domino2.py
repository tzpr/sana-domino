# coding: utf8

from random import randint
from optparse import OptionParser  # obs! deprecated module (but good for now)
# https://pypi.python.org/pypi/func_timeout/4.2.0
from func_timeout import func_timeout
from func_timeout import FunctionTimedOut



def game_output(message):
    ''' Prints messages relevant to the game play. '''
    print('  ' + message)


def get_random_word(words):
    ''' Returns random word from the words list. '''
    if words and len(words) >= 2:
        word = words[randint(0, len(words)-1)]
    elif words and len(words) == 1:
        word = words[0]
    else:
        word = None
    return word


def last_letter(word):
    ''' Return the last letter of the given word. '''
    return word[-1:]


def letters_mach(word, previous_word):
    """ Check if the first letter of the given word is the same as the last
        letter of the previous_word.
    """
    if word is None or word == '':
        return False
    elif previous_word is None:
        return True
    else:
        return word[0] == last_letter(previous_word)


def get_next_word_for_machine(words, previous_word):
    ''' Returns a word from playable_words list starting with given letter.
        Returns None if no word can be found by given letter.
    '''
    suitable_words = []
    next_word = None

    for word in words:
        if letters_mach(word, previous_word):
            suitable_words.append(word)

    if suitable_words:
        next_word = get_random_word(suitable_words)

    return next_word


def get_next_word(options, player, words, previous_word):
    ''' Finds and returns the word or None'''
    timeout = options['timer_time']
    difficulty_level = options['difficulty_level']

    if is_man(player):
        next_word = ask_word(timeout)
        if(next_word in words):
            if letters_mach(next_word, previous_word):
                game_output(player + ': ' + next_word)
                words.remove(next_word)
                return next_word
            else:
                words.remove(next_word)
                raise Exception('Eka kirjain ei ollut vika kirjain!')
        else:
            raise Exception('Sana ei ole käytettävissä!')
    else:
        if difficulty_level > 0:
            next_word = possible_random_word(difficulty_level, previous_word,
                    words)
            if next_word:
                # TODO: refactor this
                game_output(player + ': ' + next_word)
                if not letters_mach(next_word, previous_word):
                    words.remove(next_word)
                    raise Exception('Eka kirjain ei ollut vika kirjain!')
                return next_word
            else:
                raise Exception('Sanat loppuivat kesken!')
        else:
            next_word = get_next_word_for_machine(words, previous_word)
            if next_word:
                game_output(player + ': ' + next_word)
                words.remove(next_word)
                return next_word
            else:
                raise Exception('Sanat loppuivat kesken!')


def no_timeout_set_for_answer(timer_time):
    return timer_time is None or timer_time == 0


def ask_word(timer_time):
    ''' Request next word from player. '''
    def ask():
        ''' Request next word from player. '''
        return input('Anna seuraava sana: ')

    if no_timeout_set_for_answer(timer_time):
        word = ask()
    else:
        # use func_timeout module to set timeout for user input
        # https://pypi.python.org/pypi/func_timeout/4.2.0
        word = func_timeout(timer_time, ask, args=(), kwargs=None)
    return word.rstrip()


def declare_winner(player, winner_dict):
    game_output('')
    game_output('Hurraa, ' + player + ' on voitaja!')
    game_output('')
    if player in winner_dict:
        winner_dict[player] = winner_dict[player] + 1
    else:
        winner_dict[player] = 1


def is_man(player):
    return player == 'man'


# think renaming and or refactoring this one
def possible_random_word(difficulty_level, previous_word, playable_words):
    ''' Returns random word from playable_words list if random number is
        smaller than the difficulty_level given by user.
        Yes, this is a bit fuzzy.
    '''
    random_int = randint(1, 10)

    if random_int < difficulty_level:
        word = get_random_word(playable_words)
    else:
        word = get_next_word_for_machine(playable_words, previous_word)
    return word


def drop_player(player, players):
    players.remove(player)


def print_header(options):
    ''' Prints a message to console when the game starts. '''
    timer_time = options['timer_time']

    game_output('')
    game_output('* * * * * * * * * * * * * * * * * * * * * * *')
    game_output('   Game on')
    game_output('* * * * * * * * * * * * * * * * * * * * * * *')
    game_output('')

    if timer_time > 0:
        game_output('Vastausaikaa ' + str(timer_time) + ' sekuntia!')
        game_output('')


def initialize_players(computer_player_count):
    ''' Initializes player list '''
    players = []
    players.append('man') # the human factor
    for i in range(computer_player_count):
        players.append('machine' + str(i + 1))
    return players


def read_command_line_user_arguments():
    ''' Read and store predefined optional commandline arguments. Uses
        optparse module. '''
    game_options_dict = {}
    # initialize game_options_dict with default values
    game_options_dict['computer_player_count'] = 1
    game_options_dict['timer_time'] = 0
    game_options_dict['difficulty_level'] = 0
    game_options_dict['tournament_rounds'] = 0
    game_options_dict['tournament_mode'] = False

    parser = OptionParser()
    parser.add_option('-l', '--level', dest='difficulty_level',
                      help='set the game difficulty level for the computer ' +
                      'player from 1-10. When no level is set the computer ' +
                      'makes no mistakes.', type=int)
    parser.add_option('-t', '--timer', dest='timer',
                      help='set the maximum time for the answer.', type=int)
    parser.add_option('-p', '--players', dest='player_count',
                      help='set the number of computer players. ' +
                      'Note: computer players continue the game till the end! ',
                      type=int)
    parser.add_option('-r', '--rounds', dest='tournament_rounds',
                      help='set the number of rounds to be played and ' +
                      'activate the tournament mode. The winner is the ' +
                      'one who has the most wins.', type=int)

    (options, _) = parser.parse_args()

    if options.difficulty_level is not None:
        game_options_dict['difficulty_level'] = options.difficulty_level

    if options.timer is not None:
        game_options_dict['timer_time'] = options.timer

    if options.player_count is not None:
        game_options_dict['computer_player_count'] = options.player_count

    if options.tournament_rounds is not None:
        game_options_dict['tournament_rounds'] = options.tournament_rounds
        game_options_dict['tournament_mode'] = True

    return game_options_dict


def read_playable_words_from_file():
    ''' Initializes the playable words list from a text file. '''
    file_name = 'kotus_sanat.txt'
    # see https://developers.google.com/edu/python/dict-files#files for 'rU'
    f = open(file_name, 'rU')  # read text file
    words = []
    for word in f:
        words.append(word.rstrip())  # strips trailing newline
    f.close()
    return words


def play_the_game(words, options):
    ''' The game loop '''

    game_on = True
    word = None
    playable_words = words
    winner_dict = {}  # keeps count of number of wins per player
    players = initialize_players(options['computer_player_count'])
    rounds = options['tournament_rounds']
    tournament_mode = options['tournament_mode']

    print_header(options)

    while game_on:
        for player in players:
            try:
                word = get_next_word(options, player, playable_words, word)
            except FunctionTimedOut:
                game_output('Timeout!')
                drop_player(player, players)
            except Exception as bad_word_exception:
                game_output(str(bad_word_exception))
                drop_player(player, players)
            finally:
                if(len(players) == 1):
                    declare_winner(players.pop(0), winner_dict)
                    game_on = False
                    # tournament related
                    if rounds > 0:
                        rounds = rounds - 1
                        game_output('')
                        game_output('Kierroksia jäljellä: ' + str(rounds))
                        game_output('')
                        # if tournament initialize_players and word list
                        players = initialize_players(options['computer_player_count'])
                        playable_words = read_playable_words_from_file()
                        game_on = True
                        previous_word = None # reset the previous word

                    if tournament_mode and rounds == 0:
                        game_output('')
                        game_output('Turnaus päättyi!')
                        game_output(str(winner_dict))
                        game_on = False


def start_the_game():
    ''' The main function. Call others from here. '''
    words = read_playable_words_from_file()
    options = read_command_line_user_arguments()
    play_the_game(words, options)


start_the_game()
