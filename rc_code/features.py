__author__ = 'zweiss'


def get_features(count_dict, feature_file = 'features.txt'):
    """
    Returns a dictionary of features
    :param count_dict: count dictionary to calculate features on
    :param feature_file: file where list of features is saved
    :return:
    """

    return {
        'FEAT_mean_sentence_length_in_words': get_avg_sentence_length_in_words(
            count_dict['COUNTS_num_sentences'], count_dict['COUNTS_num_tokens_no_punct']),
        'FEAT_mean_word_length_in_syllables': get_avg_word_length_in_syllables(
            count_dict['COUNTS_num_tokens_no_punct'], count_dict['COUNTS_num_syllables']),
        'FEAT_mean_word_length_in_characters': get_avg_word_length_in_characters(
            count_dict['COUNTS_num_tokens_no_punct'], count_dict['COUNTS_num_characters']),
        'FEAT_avg_num_1_syllable_words': get_avg_num_1_syllable_words(
            count_dict['COUNTS_num_tokens_no_punct'], count_dict['COUNTS_num_words_1_syllable']),
        'FEAT_avg_num_3_or_more_syllable_words': get_avg_num_3_or_more_syllable_words(
            count_dict['COUNTS_num_tokens_no_punct'], count_dict['COUNTS_num_words_3_or_more_syllables']),
        'FEAT_avg_num_6_or_more_character_words': get_avg_num_6_or_more_character_words(
            count_dict['COUNTS_num_tokens_no_punct'], count_dict['COUNTS_num_words_6_or_more_characters']),
        'FEAT_sentence_word_ratio': get_sentence_word_ratio(count_dict['COUNTS_num_sentences'],
                                                            count_dict['COUNTS_num_tokens']),
        'FEAT_word_dot_ratio': get_ratio_word_to_periods_and_colons(
            count_dict['COUNTS_num_tokens_no_punct'], count_dict['COUNTS_num_periods_and_colons'])
    }


def get_avg_sentence_length_in_words(num_sentences, num_words):
    """
    Returns the average sentence length in words
    :param num_sentences: number of sentences
    :param num_words: number of words
    :return: average sentence length in words
    """

    return 0 if num_sentences == 0 else num_words / num_sentences


def get_avg_word_length_in_syllables(num_words, num_syllables):
    """
    Returns the average word length in syllables
    :param num_words: number of words
    :param num_syllables: number of syllables
    :return: average word length in syllables
    """

    return 0 if num_words == 0 else num_syllables / num_words


def get_avg_word_length_in_characters(num_words, num_characters):
    """
    Returns the average word length in characters
    :param num_words: number of words
    :param num_characters: number of characters
    :return: average word length in characters
    """

    return 0 if num_words == 0 else num_characters / num_words


def get_avg_num_1_syllable_words(num_words, num_1_syllable_words):
    """
    Returns the average number of one syllable words
    :param num_words: number of words
    :param num_1_syllable_words: number of single syllable words
    :return: average number of one syllable words
    """

    return 0 if num_words == 0 else num_1_syllable_words / num_words


def get_avg_num_3_or_more_syllable_words(num_words, num_3_or_more_syllable_words):
    """
    Returns the average number of words with three or more syllables
    :param num_words: number of words
    :param num_3_or_more_syllable_words: number of words with three or more syllables
    :return: average number of words with three or more syllables
    """

    return 0 if num_words == 0 else num_3_or_more_syllable_words / num_words


def get_avg_num_6_or_more_character_words(num_words, num_6_or_more_character_words):
    """
    Returns the average number of words with at least 6 characters
    :param num_words: number of words
    :param num_6_or_more_character_words: number of words with at least 6 characters
    :return: average number of words with at least 6 characters
    """

    return 0 if num_words == 0 else num_6_or_more_character_words / num_words


def get_ratio_word_to_periods_and_colons(num_words, num_periods_and_colons):
    """
    Returns the ratio of words to periods and colons
    :param num_words: number of words
    :param num_periods_and_colons: number of periods and colons
    :return: ratio of words to periods and colons
    """

    return 0 if num_periods_and_colons == 0 else num_words / num_periods_and_colons


def get_sentence_word_ratio(num_sentences, num_words):
    """
    Returns the ratio of sentences to words
    :param num_sentences: number of sentences
    :param num_words: number of words
    :return: ratio of sentences to words
    """

    return 0 if num_words == 0 else num_sentences / num_words


def get_word_dot_ratio(num_words, num_dots):
    """
    Returns the ratio of words to periods
    :param num_words: number of words
    :param num_dots: number of periods
    :return: ratio of words to periods
    """

    return 0 if num_dots == 0 else num_words / num_dots


