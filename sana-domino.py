# coding: utf8
''' sana-domino peli '''

from time import time
from random import randint
from optparse import OptionParser  # obs! deprecated module (but good for now)
from func_timeout import func_timeout # https://pypi.python.org/pypi/func_timeout/4.2.0
from func_timeout import FunctionTimedOut


EXCEPTION_MSG_DICT = {
    'letters_did_not_match': 'Eka kirjain ei ollut vika kirjain!',
    'invalid_word': 'Sana ei ole käytettävissä!',
    'no_words_left': 'Sanat loppuivat kesken!',
    'timeout': 'Aika loppui kesken!'
}

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

# maybe some refactoring
def get_next_word(options, player, words, previous_word):
    ''' Finds and returns the word or None'''
    timeout = options['timer_time']
    difficulty_level = options['difficulty_level']

    if is_man(player):
        next_word = ask_word(timeout)
        if next_word in words:
            if letters_mach(next_word, previous_word):
                game_output(player + ': ' + next_word)
                words.remove(next_word)
                return next_word
            else:
                words.remove(next_word)
                raise Exception(EXCEPTION_MSG_DICT['letters_did_not_match'])
        else:
            raise Exception(EXCEPTION_MSG_DICT['invalid_word'])
    else:
        if difficulty_level > 0:
            next_word = possible_random_word(difficulty_level, previous_word,
                                             words)
            if next_word:
                game_output('{}: {}'.format(player, next_word))
                if not letters_mach(next_word, previous_word):
                    words.remove(next_word)
                    raise Exception(EXCEPTION_MSG_DICT['letters_did_not_match'])
                return next_word
            else:
                raise Exception(EXCEPTION_MSG_DICT['no_words_left'])
        else:
            next_word = get_next_word_for_machine(words, previous_word)
            if next_word:
                game_output('{}: {}'.format(player, next_word))
                words.remove(next_word)
                return next_word
            else:
                raise Exception(EXCEPTION_MSG_DICT['no_words_left'])

def timeout_set_for_answer(timer_time):
    ''' Check is there a limit set for answering time. '''
    return timer_time and timer_time > 0

def ask_word(timer_time):
    ''' Request next word from player. '''
    def ask():
        ''' Request next word from player. '''
        return input('Anna seuraava sana: ')

    if timeout_set_for_answer(timer_time):
        # use func_timeout module to set timeout for user input
        # https://pypi.python.org/pypi/func_timeout/4.2.0
        word = func_timeout(timer_time, ask, args=(), kwargs=None)
    else:
        word = ask()
    return word.rstrip()

def declare_round_winner(player, winner_dict):
    ''' Print round winner and udpate winner_dict. '''
    update_winner_dict(player, winner_dict)
    print_tournament_round_winner(player)

def declare_game_winner(player):
    ''' Print game winner. '''
    print_game_winner(player)

def update_winner_dict(player, winner_dict):
    ''' Udpate tournament winner_dict. '''
    if player in winner_dict:
        winner_dict[player] = winner_dict[player] + 1
    else:
        winner_dict[player] = 1

def print_tournament_round_winner(winner):
    ''' Print tournament round winner message. '''
    game_output('')
    game_output('Hurraa, {} on kierroksen voittaja!'.format(winner))
    game_output('')

def print_game_winner(winner):
    ''' Print game winner message. '''
    game_output('')
    game_output('Hurraa, {} on pelin voittaja!'.format(winner))
    game_output('')

def print_header(options):
    ''' Prints a message to console when the game starts. '''
    timer_time = options['timer_time']
    rounds = options['tournament_rounds']
    tournament_mode = options['tournament_mode']

    if tournament_mode:
        print_tournament_start_message(rounds)
    else:
        print_game_start_message()

    if timer_time > 0:
        print_game_timeout_info(timer_time)

def print_game_start_message():
    ''' Print game start message '''
    game_output('')
    game_output('* * * * * * * * * * * * * * * * * * * * * * *')
    game_output('   Game on ')
    game_output('* * * * * * * * * * * * * * * * * * * * * * *')
    game_output('')

def print_tournament_start_message(rounds):
    ''' Print tournament start message '''
    game_output('')
    game_output('* * * * * * * * * * * * * * * * * * * * * * *')
    game_output('   Game on. Tournament! {} rounds.'.format(rounds))
    game_output('* * * * * * * * * * * * * * * * * * * * * * *')
    game_output('')

def print_game_timeout_info(timer_time):
    ''' Print game timeout info if timeout is set  '''
    game_output('Vastausaikaa {} sekuntia!'.format(timer_time))
    game_output('')

def print_tournament_end_message(winner_dict):
    ''' Print notification and info about tournament ending. '''
    game_output('Turnaus päättyi!')
    game_output('')
    game_output(find_tournament_winner(winner_dict))
    game_output('')

def print_exception_and_drop_player(player, players_dict, exception):
    ''' Post invalid_word_exception actions '''
    game_output(str(exception))
    drop_player(player, players_dict)

def print_tournament_round_info(rounds):
    ''' Print tournament round information '''
    game_output('Kierroksia jäljellä: {}'.format(rounds))
    game_output('')

def initialize_player_dict(computer_player_count):
    ''' Initializes player list '''
    players = {}
    players['man'] = 'active'
    for i in range(computer_player_count):
        players['machine' + str(i + 1)] = 'active'
    return players

def is_man(player):
    ''' Check if player type is man. '''
    return player == 'man'

# think renaming and or refactoring
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

def drop_player(player, player_dict):
    ''' Update player's state to dropped in player_dict. '''
    player_dict[player] = 'dropped'

def read_command_line_arguments():
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
    word_file = open(file_name, 'rU')  # read text file
    words = []
    for word in word_file:
        words.append(word.rstrip())  # strips trailing newline
    word_file.close()
    return words

def find_tournament_winner(winner_dict):
    ''' Get the tournament winner or winners from the winner_dict. '''
    name = ''
    wins = 0
    multiple_winners = False
    msg = ''

    for winner in winner_dict:
        if winner_dict[winner] > wins:
            name = winner
            wins = winner_dict[winner]
        elif winner_dict[winner] == wins:
            multiple_winners = True
            name = '{} ja {}'.format(name, winner)
            wins = winner_dict[winner]

    if multiple_winners:
        # https://docs.python.org/3/library/string.html#format-examples
        msg = "Voittajat {:s}, {:d} voittoa!".format(name, wins)
    else:
        msg = "Voittaja {:s}, {:d} voittoa!".format(name, wins)
    return msg

def player_active(player, player_dict):
    ''' Check is player in active state. '''
    return player_dict[player] == 'active'

def find_winner(player_dict):
    ''' Returns the player with flag on. Used when only one player left. '''
    for player in player_dict:
        if player_active(player, player_dict):
            return player

def only_one_player_left(player_dict):
    ''' Check is only one active player left in the round. '''
    number_of_active_players = 0
    for player in player_dict:
        if player_active(player, player_dict):
            number_of_active_players = number_of_active_players + 1
    return number_of_active_players == 1

def print_elapsed_time(start_time):
    ''' Prints the time spent in the game in seconds. '''
    time_gone = round((time() - start_time), 0)
    game_output('Peliin käytetty aika: {} sekuntia.'.format(time_gone))
    game_output('')

def play_the_game(words, options):
    ''' The game loop '''
    game_on = True
    word = None
    playable_words = words
    winner_dict = {}  # keeps count of wins per player
    players_dict = initialize_player_dict(options['computer_player_count'])
    rounds = options['tournament_rounds']
    tournament_mode = options['tournament_mode']
    start_time = time()

    print_header(options)

    while game_on:
        for player in players_dict:
            if player_active(player, players_dict):
                try:
                    word = get_next_word(options, player, playable_words, word)
                except FunctionTimedOut:
                    print_exception_and_drop_player(player, players_dict,
                                                    EXCEPTION_MSG_DICT['timeout'])
                except Exception as invalid_word_exception:
                    print_exception_and_drop_player(player, players_dict,
                                                    invalid_word_exception)
            if only_one_player_left(players_dict):
                # tournament related
                if tournament_mode:
                    declare_round_winner(find_winner(players_dict), winner_dict)
                    rounds = rounds - 1
                    if rounds > 0:
                        print_tournament_round_info(rounds)
                        # initialize_players and word list for the next round
                        players_dict = initialize_player_dict(options[
                            'computer_player_count'])
                        playable_words = read_playable_words_from_file()
                        game_on = True
                        word = None # reset the previous word
                    if rounds == 0:
                        print_tournament_end_message(winner_dict)
                        print_elapsed_time(start_time)
                        game_on = False
                        break
                else:
                    declare_game_winner(find_winner(players_dict))
                    print_elapsed_time(start_time)
                    game_on = False
                    break

def start_the_game():
    ''' The main function. Call others from here. '''
    words = read_playable_words_from_file()
    options = read_command_line_arguments()
    play_the_game(words, options)

# guard to only execute code when a file is invoked as a script
if __name__ == '__main__':
    start_the_game()
