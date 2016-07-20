__author__ = 'zweiss'

import nltk.data
from nltk.tokenize import WordPunctTokenizer


def get_tokenized_sentences(text):
    """
    Segmentizes and tokenizes a text
    :param text: text to be segmentized and tokenized
    :return: list of tokenized sentences
    """

    tokenized_sentences = []
    sentences = get_sentences(text)
    for sentence in sentences:
        tokenized_sentences.append(get_tokens(sentence))

    return tokenized_sentences



def get_sentences(text):
    """
    Segmentizes a text to sentences
    :param text: text to be segmentized
    :return: List of segmentized sentences
    """

    tokenizer = nltk.data.load('tokenizers/punkt/german.pickle')
    return tokenizer.tokenize(text)


def get_tokens(sentence):
    """
    Tokenizes a list of sentences
    :param sentence: list of sentences
    :return: list of tokenized sentences
    """

    tokenizer = WordPunctTokenizer()
    return tokenizer.tokenize(sentence)


def get_num_syllables(unit):
    """
    Returns the number of syllables in a given unit
    :param unit: unit to be counted
    :return: number of syllables
    """

    num_syllables = 0
    vowels = ['a', 'e', 'i', 'o', 'u', 'y', 'ü', 'ä', 'ö']
    tmp = "#" + unit.lower() + '#'  # '#' for easier iteration

    cur_char = ''
    next_char = ''
    skip = False
    for c in range(0, len(tmp)-1):

        if skip:
            skip = False
            continue

        cur_char = tmp[c]
        next_char = tmp[c+1]

        # increase number of syllables, if current character is a vowel
        if cur_char in vowels:
            num_syllables += 1

        # ignore next character, if character bigram is a diphtong, i.e.
        # the current character is a) the same as the next, b) an e, u, i or y

        if (cur_char in vowels and next_char in vowels) or cur_char == next_char:
            skip = True

    return num_syllables


def get_punctuation_list():
    """
    Returns a list of punctuation marks
    :return: list of punctuation marks
    """

    return ['.', ':', ',', ';', '!', '?', '"', '\'', '(', ')', '[', ']', '{', '}', '<', '>', '/', '\\', '-']
