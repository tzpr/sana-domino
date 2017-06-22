# sana-domino

used_words = []
playable_words = []


def read_available_words_from_file():
    ''' Initializes the playable words list from kotus_sanat.txt '''


def add_word_to_used_words(word):
    ''' Adds given word to used_words list '''
    used_words.append(word)


def is_word_playable(word):
    ''' Checks if given word is valid and not used ie. available '''
    # should think if we should maintain just one list instead of two...
    return (word not in used_words) and (word in playable_words)


def play_game():
    ''' The game loop '''



def main():
    ''' The main function. Call others from here '''
    print('Hello from main!')



# start the game
main()
