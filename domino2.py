# coding: utf8
''' sana-domino peli '''

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
        if next_word in words:
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
    ''' Check is there a limit set for answering time. '''
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


def declare_round_winner(player, winner_dict):
    ''' Print round winner and udpate winner_dict. '''
    game_output('')
    game_output('Hurraa, ' + player + ' on kierroksen voittaja!')
    game_output('')
    if player in winner_dict:
        winner_dict[player] = winner_dict[player] + 1
    else:
        winner_dict[player] = 1


def is_man(player):
    ''' Check if player type is man. '''
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


def drop_player(player, player_dict):
    ''' Update player's state to dropped in player_dict. '''
    player_dict[player] = 'dropped'


def print_header(options):
    ''' Prints a message to console when the game starts. '''
    timer_time = options['timer_time']
    rounds = options['tournament_rounds']
    tournament_mode = options['tournament_mode']

    game_output('')
    game_output('* * * * * * * * * * * * * * * * * * * * * * *')
    if tournament_mode:
        game_output('   Game on. Tournament! ' + str(rounds) + ' rounds.')
    else:
        game_output('   Game on')
    game_output('* * * * * * * * * * * * * * * * * * * * * * *')
    game_output('')

    if timer_time > 0:
        game_output('Vastausaikaa ' + str(timer_time) + ' sekuntia!')
        game_output('')


def initialize_player_dict(computer_player_count):
    ''' Initializes player list '''
    players = {}
    players['man'] = 'active' # the human factor
    for i in range(computer_player_count):
        players['machine' + str(i + 1)] = 'active'
    return players


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


def get_tournament_winner(winner_dict):
    ''' Extract the tournament winner or winners from the winner_dict. '''
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
            name = name + ' ja ' + winner
            wins = winner_dict[winner]

    if multiple_winners:
        msg = 'Voittajat ' + name + ', ' + str(wins) + ' voittoa!'
    else:
        msg = 'Voittaja ' + name + ', ' + str(wins) + ' voittoa!'
    return msg


def player_active(player, player_dict):
    ''' Check is player in active state. '''
    return player_dict[player] == 'active'


def find_winner(player_dict):
    ''' Returns the player with flag on. '''
    for player in player_dict:
        if player_active(player, player_dict):
            return player


def only_one_player_left(dropped_players_count, players_dict):
    ''' Check is only one active player left in the round. '''
    return dropped_players_count == (len(players_dict) - 1)


def end_tournament_notification(winner_dict):
    ''' Print notification and info about tournament ending. '''
    game_output('Turnaus päättyi!')
    game_output('')
    game_output(get_tournament_winner(winner_dict))
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
    dropped_players_count = 0

    print_header(options)

    while game_on:
        for player in players_dict:
            if player_active(player, players_dict):
                try:
                    word = get_next_word(options, player, playable_words, word)
                except FunctionTimedOut:
                    game_output('Timeout!')
                    drop_player(player, players_dict)
                    dropped_players_count = dropped_players_count + 1
                except Exception as invalid_word_exception:
                    game_output(str(invalid_word_exception))
                    drop_player(player, players_dict)
                    dropped_players_count = dropped_players_count + 1

            if only_one_player_left(dropped_players_count, players_dict):
                declare_round_winner(find_winner(players_dict), winner_dict)
                # tournament related
                if tournament_mode:
                    rounds = rounds - 1
                    if rounds > 0:
                        game_output('Kierroksia jäljellä: ' + str(rounds))
                        game_output('')
                        # initialize_players and word list for the next round
                        players_dict = initialize_player_dict(options['computer_player_count'])
                        playable_words = read_playable_words_from_file()
                        game_on = True
                        word = None # reset the previous word
                        dropped_players_count = 0
                    if rounds == 0:
                        end_tournament_notification(winner_dict)
                        game_on = False
                        break
                game_on = False
                break


def start_the_game():
    ''' The main function. Call others from here. '''
    words = read_playable_words_from_file()
    options = read_command_line_arguments()
    play_the_game(words, options)


start_the_game()
