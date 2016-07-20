__author__ = 'zweiss'

from os import path
from os import makedirs

from nlp import get_num_syllables
from nlp import get_punctuation_list


def get_and_save_counts(tokenized_sentences, prefix, count_file='counts.txt'):
    """
    Collects the counts given in the count file (./counts.txt)
    :param tokenized_sentences: sentences
    :param count_file: file containing the counts
    :return: dictionary of counts
    """

    count_dict = initialize_counts(count_file)
    punctuation = get_punctuation_list()

    # get number of sentences
    count_dict['num_sentences'] = len(tokenized_sentences)

    # if a prefix is given, save counts to separate files
    directory = prefix[0:prefix.rfind("/")+1]
    orig_file = prefix[prefix.rfind("/")+1:]
    out_sent = make_and_open(directory+"sentences/", orig_file+".sentences.meta", 'w')
    out_tokens = make_and_open(directory+"tokens/", orig_file+".tokens.meta", 'w')
    out_punct_colon = make_and_open(directory+"punct_colon/", orig_file+".punct_colon.meta", 'w')
    out_punct = make_and_open(directory+"punctuation/", orig_file+".punct.meta", 'w')
    out_word = make_and_open(directory+"word/", orig_file+".word.meta", "w")
    out_syll3 = make_and_open(directory+"syll3plus/", orig_file+".syll3plus.meta", "w")
    out_syll1 = make_and_open(directory+"syll1/", orig_file+".syll1.meta", "w")
    out_syll2 = make_and_open(directory+"syll2less/", orig_file+".syll2less.meta", "w")
    out_char6 = make_and_open(directory+"char6plus/", orig_file+".char6plus.meta", "w")
    c_sent = c_tok = c_punct = c_punct_colon = c_word = c_syll3 = c_syll1 = c_syll2 = c_char6 = 0

    for sentence in tokenized_sentences:
        c_sent += 1
        out_sent.write(str(c_sent) + ": " + str(sentence) + "\n\n")

        # increase number of tokens
        count_dict['COUNTS_num_tokens'] += len(sentence)

        for token in sentence:
            c_tok += 1
            out_tokens.write(str(c_tok) + ": " + token + "\n\n")

            # punctuation counts
            if token in punctuation:
                c_punct += 1
                out_punct.write(str(c_punct) + ": " + token + "\n\n")
                if token == '.' or token == ':':
                    count_dict['COUNTS_num_periods_and_colons'] += 1
                    c_punct_colon += 1
                    out_punct_colon.write(str(c_punct) + ": " + token + "\n\n")

            # word counts
            else:
                # increase number of words
                count_dict['COUNTS_num_tokens_no_punct'] += 1
                c_word += 1
                out_word.write(str(c_word) + ": " + token + "\n\n")

                # syllable counts
                num_syllables = get_num_syllables(token)
                # increase total number of syllables
                count_dict['COUNTS_num_syllables'] += num_syllables
                # either 3 or more syllables
                if num_syllables > 2:
                    count_dict['COUNTS_num_words_3_or_more_syllables'] += 1
                    c_syll3 += 1
                    out_syll3.write(str(c_syll3) + " ("+str(num_syllables)+"): " + token + "\n\n")
                # or 2 or less syllables
                elif num_syllables > 0:
                    count_dict['COUNTS_num_words_2_or_less_syllables'] += 1
                    c_syll2 += 1
                    out_syll2.write(str(c_syll2) + " ("+str(num_syllables)+"): " + token + "\n\n")
                    # maybe only single syllable
                    if num_syllables == 1:
                        count_dict['COUNTS_num_words_1_syllable'] += 1
                        c_syll1 += 1
                        out_syll1.write(str(c_syll1) + " ("+str(num_syllables)+"): " + token + "\n\n")

                # character counts
                num_char = len(token)
                # increase total number of characters
                count_dict['COUNTS_num_characters'] += num_char
                # maybe 6 or more characters
                if num_char > 5:
                    count_dict['COUNTS_num_words_6_or_more_characters'] += 1
                    c_char6 += 1
                    out_char6.write(str(c_char6) + ": " + token + "\n\n")

    out_sent.close()
    out_tokens.close()
    out_punct.close()
    out_punct_colon.close()
    out_word.close()
    out_syll1.close()
    out_syll2.close()
    out_syll3.close()
    out_char6.close()

    out_counts = make_and_open(directory+"counts/", "counts.csv", 'a')
    out_counts.write(orig_file + ",")
    for key in sorted(count_dict.keys()):
        out_counts.write(str(count_dict[key]) + ",")
    out_counts.write("\n")
    out_counts.close()

    return count_dict


def make_and_open(directory, file, option):
    """
    Creates a file / directory if necessary and opens a file
    :param directory: directory
    :param file: file name
    :param option: reading, appending, writing, etc.
    :return: file stream
    """

    if not path.exists(directory):
        makedirs(directory)
    return open(directory+file, option)


def get_counts(sentences, count_file='counts.txt'):
    """
    Collects the counts given in the count file (./counts.txt)
    :param sentences: sentences
    :param count_file: file containing the counts
    :return: dictionary of counts
    """

    count_dict = initialize_counts(count_file)
    punctuation = get_punctuation_list()

    # get number of sentences
    count_dict['COUNTS_num_sentences'] = len(sentences)

    for sentence in sentences:

        # increase number of tokens
        count_dict['COUNTS_num_tokens'] += len(sentence)

        for token in sentence:

            # punctuation counts
            if token in punctuation:
                if token == '.' or token == ':':
                    count_dict['COUNTS_num_periods_and_colons'] += 1

            # word counts
            else:
                # increase number of words
                count_dict['COUNTS_num_tokens_no_punct'] += 1

                # syllable counts
                num_syllables = get_num_syllables(token)
                # increase total number of syllables
                count_dict['COUNTS_num_syllables'] += num_syllables
                # either 3 or more syllables
                if num_syllables > 2:
                    count_dict['COUNTS_num_words_3_or_more_syllables'] += 1
                # or 2 or less syllables
                elif num_syllables > 0:
                    count_dict['COUNTS_num_words_2_or_less_syllables'] += 1
                    # maybe only single syllable
                    if num_syllables == 1:
                        count_dict['COUNTS_num_words_1_syllable'] += 1

                # character counts
                num_char = len(token)
                # increase total number of characters
                count_dict['COUNTS_num_characters'] += num_char
                # maybe 6 or more characters
                if num_char > 5:
                    count_dict['COUNTS_num_words_6_or_more_characters'] += 1

    return count_dict


def initialize_counts(count_file):
    """
    Sets up the counts initialized to zero, that are given in the count file
    :param count_file: file containing all counts separated by lines
    :return: dictionary with all counts from count_file as keys, initialized to zero
    """

    count_dict = {}
    # read count dictionary keys from count_file and initialize them with
    file_reader = open(count_file, 'r')
    for line in file_reader.readlines():
        count_dict["COUNTS_" + line.strip()] = 0
    file_reader.close()

    return count_dict
