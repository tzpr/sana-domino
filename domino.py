# sana-domino
''' sana-domino - play domino with words!'''

from random import randint
from optparse import OptionParser # obs! deprecated module (but good for now)
from func_timeout import func_timeout # https://pypi.python.org/pypi/func_timeout/4.2.0
from func_timeout import FunctionTimedOut


def read_available_words_from_file(file_name):
    ''' Initializes the playable words list from a text file. '''
    word_file = open(file_name, 'rt') # read text file, rt
    words = []
    for word in word_file:
        words.append(word.rstrip()) # strips trailing newline
    word_file.close()
    return words


def remove_word_from_playable_words(word, playable_words):
    ''' Removes the given word from playable_words list. '''
    try:
        playable_words.remove(word)
    except ValueError as value_error:
        print('Carry on', value_error)


def add_word_to_used_words(word, used_words):
    ''' Adds given word to used_words list. '''
    used_words.append(word)


def last_letter(word):
    ''' Return the last letter of the given word. '''
    return word[-1:]


def get_random_word(words):
    ''' Returns random word from the words list. '''
    return words[randint(0, len(words))]


def letters_mach(word, previous_word):
    """ Check if the first letter of the given word is the same as the last
        letter of the previous_word.
    """
    return word[0] == last_letter(previous_word)


def get_next_word(previous_word, playable_words):
    ''' Returns a word from playable_words list starting with given letter.
        Removes returned word from playable_words list and ads it to the
        used_words list.
        Returns empty string if no word can be found by given letter.
    '''
    suitable_words = []
    the_word = None

    for word in playable_words:
        if letters_mach(word, previous_word):
            suitable_words.append(word)

    if suitable_words:
        the_word = get_random_word(suitable_words)

    if the_word:
        remove_word_from_playable_words(the_word, playable_words)
        return the_word

    return ''


def is_word_valid(previous_word, word):
    ''' Checks that the word starts with the same letter as the previous word
        ended.
    '''
    # inner helper methods, just for fun. could be moved to some util module.
    def the_word_does_not_exist(word):
        return word == '' or word is None

    def the_words_exist(previous_word, word):
        return (previous_word and word)

    if the_word_does_not_exist(word):
        return False

    if the_words_exist(previous_word, word):
        return letters_mach(word, previous_word)

    return True


def is_word_playable(word, playable_words, used_words):
    ''' Checks if the given word is not used and is among playable_words'''
    return (word not in used_words) and (word in playable_words)


def no_timeout_set_for_answer(timer_time):
    return timer_time is None or timer_time == 0


def ask_word(timer_time):
    ''' Asks user input. Reads next word from commandline. '''
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


def game_output(message):
    ''' Prints messages relevant to the game play. '''
    print(message)


def print_header(timer_time):
    ''' Prints a message to console when the game starts. '''
    game_output('')
    game_output('* * * * * * * * * * * * * * * * * * * * * * *')
    game_output('   Game on')
    game_output('* * * * * * * * * * * * * * * * * * * * * * *')

    if timer_time > 0:
        game_output('')
        game_output('Vastausaikaa ' + str(timer_time) + ' sekuntia!')
        game_output('')
    else:
        game_output('')


def print_tournament_results(players):
    ''' Prints tournament results so we see who is the winner. '''
    game_output(' * * * Tournament results * * * ')
    for player in players:
        game_output(' - ' + player + ' ' + str(players[player]) +
                    ' lost games.')


def game_end(message, loosing_player, options, players):
    ''' When game ends decides the next actions. '''
    #global tournament_rounds
    #global player_dict

    options['tournament_rounds'] -= 1

    if options['tournament_rounds'] > 0:
        players[loosing_player] += 1
        game_output('')
        game_output(message)
        game_output('You have lost ' + str(players[loosing_player]) +
                    ' rounds')
        game_output(str(options['tournament_rounds']) + ' rounds left to play!')
        game_output('')
        return False
    else:
        if options['tournament_mode']:
            players[loosing_player] += 1
            game_output('')
            game_output(message)
            game_output('You have lost ' + str(players[loosing_player]) +
                        ' rounds')
            game_output('')
            print_tournament_results(players)
            game_output('')
        else:
            game_output('')
            game_output(message)
        return True


def initialize_players(computer_player_count):
    ''' Initializes player dictionary for some game statistics. '''
    player_dict = {}
    player_dict['man'] = 0
    for i in range(computer_player_count):
        player_dict['machine' + str(i + 1)] = 0
    return player_dict

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
        word = get_next_word(previous_word, playable_words)
    return word


def play_the_game(words, options):
    ''' The game loop '''
    previous_word = None
    playable_words = words
    used_words = []
    timeout = options['timer_time']
    difficulty_level = options['difficulty_level']
    computer_player_count = options['computer_player_count']
    players = initialize_players(options['computer_player_count'])

    print_header(timeout)

    # the loop
    while playable_words:
        try:
            human_word = ask_word(timeout)
        except FunctionTimedOut:
            if game_end('Timeout! You lost, sorry.', 'man', options, players):
                break

        if(is_word_valid(previous_word, human_word) and is_word_playable(
                human_word, playable_words, used_words)):
            game_output('man: ' + human_word)
            previous_word = human_word
            remove_word_from_playable_words(human_word, playable_words)
            add_word_to_used_words(human_word, used_words)
            # let the machines play
            for i in range(computer_player_count):
                if difficulty_level > 0:
                    computer_word = possible_random_word(difficulty_level,
                                                         previous_word,
                                                         playable_words)
                    add_word_to_used_words(computer_word, used_words)
                else:
                    computer_word = get_next_word(previous_word,
                                                  playable_words)
                    add_word_to_used_words(computer_word, used_words)

                if is_word_valid(previous_word, computer_word):
                    game_output('machine' + str(i + 1) + ': ' + computer_word)
                    previous_word = computer_word
                else:
                    game_output('machine' + str(i + 1) + ': ' + computer_word)
                    if(game_end('Hurraa! You won, machine lost.', 'machine' +
                                str(i), options, players)):
                        return
        else:
            if game_end('Game over! You lost, sorry.', 'man', options, players):
                break


def read_command_line_user_arguments():
    ''' Read and store predefined optional commandline arguments. Uses
        optparse module. '''
    args_dictionary = {}
    # initialize with default values
    args_dictionary['computer_player_count'] = 1
    args_dictionary['timer_time'] = 0
    args_dictionary['difficulty_level'] = 0
    args_dictionary['tournament_rounds'] = 0
    args_dictionary['tournament_mode'] = False

    parser = OptionParser()
    parser.add_option('-l', '--level', dest='difficulty_level',
                      help='Difficulty level for computer (1-10)', type=int)
    parser.add_option('-t', '--timer', dest='timer',
                      help='Timeout for one move', type=int)
    parser.add_option('-p', '--players', dest='player_count',
                      help='Number of computer players', type=int)
    parser.add_option('-r', '--rounds', dest='tournament_rounds',
                      help='Tournament mode. Give number of rounds.', type=int)

    (options, _) = parser.parse_args()

    if options.difficulty_level is not None:
        args_dictionary['difficulty_level'] = options.difficulty_level

    if options.timer is not None:
        args_dictionary['timer_time'] = options.timer

    if options.player_count is not None:
        args_dictionary['computer_player_count'] = options.player_count

    if options.tournament_rounds is not None:
        args_dictionary['tournament_rounds'] = options.tournament_rounds
        args_dictionary['tournament_mode'] = True

    return args_dictionary


def start_the_game():
    ''' The main function. Call others from here. '''
    words = read_available_words_from_file('kotus_sanat.txt')
    options = read_command_line_user_arguments()
    play_the_game(words, options)

# start the game
start_the_game()
