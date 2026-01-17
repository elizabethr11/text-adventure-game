import string
from items import *

# divider used to separate turns for clarity
divider = "-------------------------------------------------------"

# List of "unimportant" words
skip_words = ['a', 'about', 'all', 'an', 'another', 'any', 'around', 'at',
              'bad', 'beautiful', 'been', 'better', 'big', 'can', 'every', 'for',
              'from', 'good', 'have', 'her', 'here', 'hers', 'his', 'how',
              'i', 'if', 'in', 'into', 'is', 'it', 'its', 'large', 'later',
              'like', 'little', 'main', 'me', 'mine', 'more', 'my', 'now',
              'of', 'off', 'oh', 'on', 'please', 'small', 'some', 'soon',
              'that', 'the', 'then', 'this', 'those', 'through', 'till', 'to',
              'towards', 'until', 'us', 'want', 'we', 'what', 'when', 'why',
              'wish', 'with', 'would']

# list of contraband items (and their ids) - used in search player/cell functions
contraband_list = ["item_medicine", "item_screwdriver", "item_money", "item_key", "item_food", "item_batteries", "item_spoon"]
contraband_list_ids = ["medicine", "screwdriver", "money", "key", "food", "batteries", "spoon"]

def filter_words(words: list, skip_words: list) -> list:
    """This function takes a list of words and returns a copy of the list with words from skip_words removed."""

    filtered_words = []
    for word in words:
        if word not in skip_words:
            filtered_words.append(word)

    return filtered_words

def remove_punct(text: str) -> str:
    """This function removes all punctuation from a given string"""

    no_punct = ""
    for char in text:
        if not (char in string.punctuation):
            no_punct = no_punct + char

    return no_punct


def normalise_input(user_input: str, win: bool=False) -> list | str:
    """This function normalises the user's input so that it can be 
        used to direct what they want to do"""

    # Remove punctuation and convert to lower case
    no_punct = remove_punct(user_input).lower()

    # removes whitespace and converts it to a list of words
    words = (no_punct.strip()).split()

    # removes unnecessary words
    if not win:
        return filter_words(words, skip_words)
    else:
        return no_punct