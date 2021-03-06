# coding: utf8
''' sana-domino peli '''

from time import time
from random import randint
from optparse import OptionParser  # obs! deprecated module (but good for now)
from func_timeout import func_timeout # https://pypi.python.org/pypi/func_timeout/4.2.0
from func_timeout import FunctionTimedOut


# global variable that holds the error messages shown to player
EXCEPTION_MSG_DICT = {
    'letters_did_not_match': 'Eka kirjain ei ollut vika kirjain!',
    'invalid_word': 'Sana ei ole käytettävissä!',
    'no_words_left': 'Sanat loppuivat kesken!',
    'timeout': 'Aika loppui kesken!'
}

def game_output(message):
    ''' Prints messages relevant to the game play. '''
    print('  ' + message)

def random_word(words):
    ''' Returns random word from the words list or None if no words left. '''
    if words and len(words) >= 2:
        word = words[randint(0, len(words)-1)]
    elif words and len(words) == 1:
        word = words[0]
    else:
        word = None
    return word

def first_letter_is_last_letter(new_word, previous_word):
    """ Check if the first letter of the new_word is the same as the last
        letter of the previous_word.
    """
    if new_word is None or new_word == '':
        return False
    elif previous_word is None:
        return True
    return new_word[0] == previous_word[-1:]

def get_next_word_for_machine(playable_words, previous_word, difficulty_level):
    ''' Returns a word from playable_words list starting with given letter.
        Returns random word if diffculty level is set and randomnes occures.
        None is returned if no words are left in playable_words list.
    '''
    suitable_words = []
    # handle possible random word
    if difficulty_level and difficulty_level > 0:
        random_int = randint(1, 10)
        if random_int < difficulty_level:
            return random_word(playable_words)
    # try to find possible playable words
    for word in playable_words:
        if first_letter_is_last_letter(word, previous_word):
            suitable_words.append(word)
    return random_word(suitable_words)

def get_next_word(difficulty_level, player, playable_words, previous_word):
    ''' The next word. '''
    if player_human(player):
        next_word = input('Anna seuraava sana: ').rstrip()
    else:
        next_word = get_next_word_for_machine(playable_words, previous_word,
                                              difficulty_level)
    return next_word

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

def print_tournament_round_winner(player):
    ''' Print tournament round winner message. '''
    game_output('')
    game_output('Hurraa, {} on kierroksen voittaja!'.format(player))
    game_output('')

def print_game_winner(player):
    ''' Print game winner message. '''
    game_output('')
    game_output('Hurraa, {} on pelin voittaja!'.format(player))
    game_output('')

def print_header(options):
    ''' Prints a message to console when the game starts. '''
    time_limit = options['timer_time']
    rounds = options['tournament_rounds']
    tournament_mode = options['tournament_mode']

    if tournament_mode:
        print_tournament_start_message(rounds)
    else:
        print_game_start_message()

    if time_limit > 0:
        print_game_time_limit_info(time_limit)

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

def print_game_time_limit_info(time_limit):
    ''' Print game timeout info if timeout is set  '''
    game_output('Vastausaikaa {} sekuntia!'.format(time_limit))
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
    game_output('')

def print_tournament_round_info(num_of_rounds):
    ''' Print tournament round information '''
    game_output('Kierroksia jäljellä: {}'.format(num_of_rounds))
    game_output('')

def initialize_player_dict(computer_player_count):
    ''' Initializes player list '''
    players = {}
    players['man'] = 'active'
    for i in range(computer_player_count):
        players['machine' + str(i + 1)] = 'active'
    return players

def player_human(player):
    ''' Check if player type is man. '''
    return player == 'man'

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

    # https://docs.python.org/2/library/optparse.html
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
    # get the options, discard the leftover arguments with _
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
    ''' Initializes the playable words list from a file (kotus_sanat.txt). '''
    file_name = 'kotus_sanat.txt'
    # see https://developers.google.com/edu/python/dict-files#files for 'rU'
    word_file = open(file_name, 'rU')  # read text file
    words = []
    for word in word_file:
        words.append(word.rstrip())  # strips trailing newline
    word_file.close()
    return words

def find_tournament_winner(winner_dict):
    ''' Resolve the tournament winner or winners from the winner_dict. '''
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
    ''' Check if player is in active state. '''
    return player_dict[player] == 'active'

def find_winner(player_dict):
    ''' Returns the active player. Used when only one player is left. '''
    for player in player_dict:
        if player_active(player, player_dict):
            return player

def only_one_player_left(player_dict):
    ''' Check if only one active player is left in the round. '''
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

# refactor?
def validate(player, word, previous_word, playable_words):
    if word:
        if word in playable_words:
            game_output('{}: {}'.format(player, word))
            if first_letter_is_last_letter(word, previous_word):
                playable_words.remove(word)
                return word
            else:
                playable_words.remove(word)
                raise Exception(EXCEPTION_MSG_DICT['letters_did_not_match'])
        else:
            raise Exception(EXCEPTION_MSG_DICT['invalid_word'])
    else:
        raise Exception(EXCEPTION_MSG_DICT['no_words_left'])

def play_the_game(words, options):
    ''' The game loop '''
    # variable that controls whether the game is on or not
    game_on = True
    # stores the latest played word (by man or machine)
    previous_word = None
    # list of words available for the ongoing game
    playable_words = words
    # stores the winners and keeps count of wins per tournament
    winner_dict = {}
    # variable that holds the players and their state (active/dropped)
    players_dict = initialize_player_dict(options['computer_player_count'])
    # number of rounds to be played, decreased after each game round
    rounds = options['tournament_rounds']
    # convinience flag that tells whether game is in tournament mode or not (True/False)
    tournament_mode = options['tournament_mode']
    # time limit for player's move in seconds. Defaults to 2 minutes.
    time_limit = options['timer_time'] or 120
    # difficulty level for machine players, used to randomize machine's answer.
    difficulty_level = options['difficulty_level']
    # used to count the time spent in the game or tournament. Extra.
    game_start_time = time()

    print_header(options)

    while game_on:
        for player in players_dict:
            if player_active(player, players_dict):
                try:
                    # use func_timeout module to trigger time limit
                    word = func_timeout(time_limit, get_next_word,
                                        args=(difficulty_level, player, playable_words,
                                              previous_word), kwargs=None)
                    previous_word = validate(player, word, previous_word, playable_words)
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
                        previous_word = None # reset the previous word
                    if rounds == 0:
                        print_tournament_end_message(winner_dict)
                        print_elapsed_time(game_start_time)
                        game_on = False
                        break
                else:
                    declare_game_winner(find_winner(players_dict))
                    print_elapsed_time(game_start_time)
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
