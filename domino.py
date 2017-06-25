# sana-domino

import random
import math
import optparse # parse commandline parameters
import func_timeout # https://pypi.python.org/pypi/func_timeout/4.2.0


# global variables
used_words = []
playable_words = []
timer_time = 0
computer_player_count = 1
tournament_rounds = 0
FILE_NAME = 'kotus_sanat.txt'
player_dict = {}
tournament_mode = False
difficulty_level = 0


def read_available_words_from_file():
    ''' Initializes the playable words list from kotus_sanat.txt '''
    word_file = open(FILE_NAME, 'rt') # read text file
    for word in word_file:
        playable_words.append(word.rstrip()) # strips trailing newline
    word_file.close()


def remove_word_from_playable_words(word):
    ''' Removes the given word from playable_words list. '''
    try:
        global playable_words
        playable_words.remove(word)
    except ValueError as ve:
        print('Carry on', ve)


def add_word_to_used_words(word):
    ''' Adds given word to used_words list. '''
    used_words.append(word)


def last_letter(word):
    ''' Return the last letter of the given word. '''
    return word[len(word) - 1]


def get_random_word(words):
    ''' Returns random word from the words list. '''
    return words[random.randint(0, len(words))]


def get_next_word(previous_word):
    ''' Returns a word from playable_words list starting with given letter.
        Removes returned word from playable_words list and ads it to the
        used_words list.
        Returns empty string if no word can be found by given letter.
    '''
    suitable_words = []
    the_word = None

    for word in playable_words:
        if(word[0] == last_letter(previous_word)):
            suitable_words.append(word)

    if(len(suitable_words) > 0):
        the_word = get_random_word(suitable_words)

    if(the_word is not None):
        remove_word_from_playable_words(the_word)
        add_word_to_used_words(the_word)
        return the_word

    return ''


def is_word_valid(previous_word, word):
    ''' Checks that the word starts with the same letter as the previous word
        ended.
    '''
    if(word == '' or word is None):
        return False

    if(previous_word is not None and word is not None):
        return last_letter(previous_word) == word[0]

    return True


def is_word_playable(word):
    ''' Checks if the given word is not used and is among playable_words'''
    return (word not in used_words) and (word in playable_words)

def timeout_message():
    print('Timeout, sorry.')



def ask_word(timer_time):
    ''' Asks user input. Reads next word from commandline. '''

    def ask():
        return input('Anna seuraava sana: ')

    if(timer_time is None or timer_time == 0):
        word = ask()
    else:
        # use func_timeout module to set timeout for user input
        word = func_timeout.func_timeout(timer_time, ask, args=(),
                kwargs=None)

    return word.rstrip()


def print_header():
    ''' Prints a message to console when the game starts. '''

    print('')
    print('* * * * * * * * * * * * * * * * * * * * * * *')
    print('   Game on')
    print('* * * * * * * * * * * * * * * * * * * * * * *')

    if(timer_time > 0):
        print('')
        print('Vastausaikaa ' + str(timer_time) + ' sekuntia!')
        print('')
    else:
        print('')


def print_tournament_results():
    print(' * * * Tournament results * * * ')
    for player in player_dict:
        print( ' - ' + player + ' ' + str(player_dict[player]) +
                ' lost games.')


def game_end(message, loosing_player):
    global tournament_rounds
    global player_dict

    tournament_rounds -= 1

    if(tournament_rounds > 0):
        player_dict[loosing_player] += 1
        print('')
        print(message)
        print('You have lost ' + str(player_dict[loosing_player]) + ' rounds')
        print( str(tournament_rounds) + ' rounds left to play!')
        print('')
        return False
    else:
        if(tournament_mode):
            player_dict[loosing_player] += 1
            print('')
            print(message)
            print('You have lost ' + str(player_dict[loosing_player]) +
                    ' rounds')
            print('')
            print_tournament_results()
            print('')
        else:
            print('')
            print(message)
        return True


def initialize_players():
    ''' Initializes player dictionary for some game statistics. '''
    if(tournament_mode):
        global player_dict
        player_dict['man'] = 0
        for i in range(computer_player_count):
            player_dict['machine' + str(i + 1)] = 0


def possible_random_word(difficulty_level, previous_word):
    ''' Returns random word from playable_words list if random number is
        smaller than difficulty_level. Yes, there is no logic in this.
    '''
    random_int = random.randint(1, 10)

    if(random_int < difficulty_level):
        #print('Random word!')
        return get_random_word(playable_words)
    else:
        #print('Not so random word!')
        return get_next_word(previous_word)


def play_game():
    ''' The game loop '''
    previous_word = None

    print_header()
    initialize_players()

    # the beginning
    while len(playable_words) > 0:
        try:
            human_word = ask_word(timer_time)
        except func_timeout.exceptions.FunctionTimedOut:
            if(game_end('Timeout! You lost, sorry.', 'man')):
                break

        if(is_word_valid(previous_word, human_word) and is_word_playable(
                human_word)):
            print('man: ' + human_word)
            previous_word = human_word
            remove_word_from_playable_words(human_word)
            add_word_to_used_words(human_word)
            # let the machines play
            for i in range(computer_player_count):
                if(difficulty_level > 0):
                    computer_word = possible_random_word(difficulty_level,
                            previous_word)
                else:
                    computer_word = get_next_word(previous_word)

                if(is_word_valid(previous_word, computer_word)):
                    print('machine' + str(i + 1) + ': ' + computer_word)
                    previous_word = computer_word
                else:
                    print('machine' + str(i + 1) + ': ' + computer_word)
                    if(game_end('Hurraa! You won, machine lost.', 'machine' +
                            str(i))):
                        return
        else:
            if(game_end('Game over! You lost, sorry.', 'man')):
                break


def read_arguments():
    ''' Read and store predefined optional commandline arguments. '''

    parser = optparse.OptionParser()
    parser.add_option('-l', '--level', dest='difficulty_level',
            help='Difficulty level for computer (1-10)', type=int)
    parser.add_option('-t', '--timer', dest='timer',
            help='Timeout for one move', type=int)
    parser.add_option('-p', '--players', dest='player_count',
            help='Number of computer players', type=int)
    parser.add_option('-r', '--rounds', dest='tournament_rounds',
            help='Tournament mode. Give number of rounds.', type=int)

    (options, args) = parser.parse_args()

    if(options.difficulty_level is not None):
        print('LEVEL: ' + str(options.difficulty_level))
        global difficulty_level
        difficulty_level = options.difficulty_level

    if(options.timer is not None):
        print('TIMER: ' + str(options.timer))
        global timer_time
        timer_time = options.timer

    if(options.player_count is not None):
        print('PLAYER COUNT: ' + str(options.player_count))
        global computer_player_count
        computer_player_count = options.player_count

    if(options.tournament_rounds is not None):
        print('TOURNAMENT ROUNDS: ' + str(options.tournament_rounds))
        global tournament_rounds
        global tournament_mode
        tournament_rounds = options.tournament_rounds
        tournament_mode = True

def main():
    ''' The main function. Call others from h2ere '''
    read_available_words_from_file()
    read_arguments()
    play_game()

# start the game
main()
