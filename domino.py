# sana-domino

import random, math

used_words = []
playable_words = []
file_name = 'kotus_sanat.txt'


def read_available_words_from_file():
    ''' Initializes the playable words list from kotus_sanat.txt '''
    word_file = open(file_name, 'rt') # read text file
    for word in word_file:
        playable_words.append(word.rstrip()) # strips all kinds of trailing whitespace by default, including newline
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
    ''' Checks if the given word is not used '''
    # can human player use words outside the playable_words list?
    return (word not in used_words) and (word in playable_words)


def ask_word():
    word = input('Anna seuraava sana: ')
    return word.rstrip()


def play_game():
    ''' The game loop '''

    print('* * * * * * * * * * * * * * * * * * * * * * *')
    print('   Game on')
    print('* * * * * * * * * * * * * * * * * * * * * * *')
    previous_word = ''

    # the beginning
    human_word = ask_word()
    if(is_word_valid(None, human_word) and is_word_playable(human_word)):
        print('man: ' + human_word)
        previous_word = human_word
        remove_word_from_playable_words(human_word)
        computer_word = get_next_word(human_word)
        if(is_word_valid(previous_word, computer_word)):
            print('machine: ' + computer_word)
            previous_word = computer_word
        else:
            print('Hurraa! You won, machine lost.')
    else:
        print('Game over! You lost, sorry.')

    while len(playable_words) > 0:
        human_word = ask_word()
        if(is_word_valid(previous_word, human_word) and is_word_playable(human_word)):
            print('man: ' + human_word)
            previous_word = human_word
            remove_word_from_playable_words(human_word)
            computer_word = get_next_word(human_word)
            if(is_word_valid(previous_word, computer_word)):
                print('machine: ' + computer_word)
                previous_word = computer_word
            else:
                print('Hurraa! You won, machine lost.')
        else:
            print('Game over! You lost, sorry.')
            break

def main():
    ''' The main function. Call others from here '''
    #print('Hello from main!')
    read_available_words_from_file()
    play_game()


# start the game
main()
