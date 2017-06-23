
# Smallish testsuite for domino.py

# import the functionality to be tested from the domino.py file
from domino import read_available_words_from_file
from domino import playable_words
from domino import used_words
from domino import get_next_word
from domino import is_word_playable
from domino import is_word_valid
from domino import remove_word_from_playable_words


passed_tests = 0
failed_tests = 0

def verdict(ok):
    if(ok):
        global passed_tests # use global to modify attribute not defined in the function
        passed_tests += 1
        return 'PASSED'
    else:
        global failed_tests # use global to modify attribute not defined in the function
        failed_tests += 1
        return 'FAILED'


print('')
print('')
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
print('    TEST SUITE for sana-domino')
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
print('')

# test file reading
print('TEST read words from a text file.')
read_available_words_from_file()
print(' - read words from a file: ' + verdict(len(playable_words) > 90000))
print('')

# test getting next word
print('TEST get next word by last letter of the previous word. Word found.')
word = get_next_word('omenapuu')
print(' - a word starting with u: ' + word + ' ' + verdict(word is not ''))
print(' - the word should be removed from playable_words: ' + verdict(word not in playable_words))
print(' - the word should be added to used_words: ' + verdict(word in used_words))
print('')

# test getting next word, not found
print('TEST get next word by last letter of the previous word. Word not found.')
word = get_next_word('alabama_')
print(' - empty string should be returned if no word is found: ' + verdict(word == ''))
print('')

# test if a word is playable
print('TEST word playability check')
print(' - word should be playable, öljy ' + verdict(is_word_playable('öljy')))
used_words.append('öljy')
playable_words.remove('öljy')
print(' - word should not be playable, öljy ' + verdict(not is_word_playable('öljy')))
print(' - word should be playable, öljysheikki ' + verdict(is_word_playable('öljysheikki')))
print(' - word should be playable, öylätti ' + verdict(is_word_playable('öylätti')))
playable_words.remove('öylätti')
print(' - word should not be playable, öylätti ' + verdict(not is_word_playable('öylätti')))
print('')

# test word validation
print('TEST word validation')
print(' - word should be ok, (omena, aatami) ' + verdict(is_word_valid('omena', 'aatami')))
print(' - word should not be ok, (omena, emilia) ' + verdict(not is_word_valid('omena', 'emilia')))
print('')

# test word removal
print('TEST word removal from playable_words list')
remove_word_from_playable_words('auto')
print(' - word should not be playable, auto ' + verdict(not is_word_playable('auto')))


print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
print(' Tests PASSED: ' + str(passed_tests) + ' Tests FAILED: ' + str(failed_tests))
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
print('')
