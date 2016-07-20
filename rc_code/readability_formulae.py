__author__ = 'zweiss'


def get_formulae(features):
    """
    Caluclates readability formulae
    :param features: feature dictionary used for formula calculation
    :return: dictionary with readability formulae
    """

    return {
        'FLESCH_amstad_readability_index': amstad_lesbarkeits_index(
            features['FEAT_mean_sentence_length_in_words'], features['FEAT_mean_word_length_in_syllables']),
        'FLESCH_flesch_reading_ease': flesch_reading_ease(
            features['FEAT_mean_sentence_length_in_words'], features['FEAT_mean_word_length_in_syllables']),
        'FLESCH_flesch_kincaid_grade_level': flesch_kincaid_grade_level(
            features['FEAT_mean_sentence_length_in_words'], features['FEAT_mean_word_length_in_syllables']),

        'VIENNA_1st_vienna_formula_for_factual_texts': erste_wiener_sachtextformel(
            features['FEAT_avg_num_3_or_more_syllable_words'], features['FEAT_mean_sentence_length_in_words'],
            features['FEAT_avg_num_6_or_more_character_words'], features['FEAT_avg_num_1_syllable_words']),
        'VIENNA_2nd_vienna_formula_for_factual_texts': zweite_wiener_sachtextformel(
            features['FEAT_avg_num_3_or_more_syllable_words'], features['FEAT_mean_sentence_length_in_words'],
            features['FEAT_avg_num_6_or_more_character_words']),
        'VIENNA_3rd_vienna_formula_for_factual_texts': dritte_wiener_sachtextformel(
            features['FEAT_avg_num_3_or_more_syllable_words'], features['FEAT_mean_sentence_length_in_words']),
        'VIENNA_4th_vienna_formula_for_factual_texts': vierte_wiener_sachtextformel(
            features['FEAT_avg_num_3_or_more_syllable_words'], features['FEAT_mean_sentence_length_in_words']),

        'OTHER_lix_readability_index': lix_lesbarkeitsindex(
            features['FEAT_mean_sentence_length_in_words'], features['FEAT_avg_num_6_or_more_character_words']),
        # 'OTHER_g_smog_index': g_smog_index(
        #     features['FEAT_avg_num_3_or_more_syllable_words'], features['COUNTS_num_sentences']),
        'OTHER_gunning_fog_index': gunning_fog_index(
            features['FEAT_mean_sentence_length_in_words'], features['FEAT_avg_num_3_or_more_syllable_words']),
        'OTHER_coleman_liau_index': coleman_liau_index(
            features['FEAT_mean_word_length_in_characters'], features['FEAT_sentence_word_ratio']),
        'OTHER_automated_readability_index': automated_readability_index(
            features['FEAT_mean_word_length_in_characters'], features['FEAT_mean_sentence_length_in_words']),

        'L2_miyazaki_efl_readability_index': miyazaki_efl_readability_index(
            features['FEAT_mean_word_length_in_characters'], features['FEAT_mean_sentence_length_in_words'])
    }


# =====================================================================================================================
# Flesch based formulae
# =====================================================================================================================


def flesch_helper(epsilon, param_mean_sent_length, param_mean_num_syllables_per_word):
    """
    Helper calculating Flesch formulae using different parameters
    :param epsilon: epsilon parameter
    :param param_mean_sent_length: parameterized mean sentence length in words
    :param param_mean_num_syllables_per_word: parameterized mean number of syllables per word
    :return: Flesch index
    """

    # compute index
    return epsilon - param_mean_sent_length - param_mean_num_syllables_per_word


def amstad_lesbarkeits_index(mean_sent_length, mean_num_syllables_per_word):
    """
    The Amstad Readability Index is based on the Flesch formulae for English. However, its parameters were adjusted for
    German by Amstad (1978).

    The formula is:
        180 - mean sentence length - mean number of syllables per word * 58.5

    The index ranges between 0 and infinity, higher values indicating lower text difficulty. According to XX, average
    text difficulty for German is indicated by a value of XX.

    :param mean_sent_length: mean sentence length in words
    :param mean_num_syllables_per_word: mean number of syllables per word
    :return: the readability index > 0
    """

    return flesch_helper(180, mean_sent_length, mean_num_syllables_per_word * 58.5)


def flesch_reading_ease(mean_sent_length, mean_num_syllables_per_word):
    """
    The Flesch Reading Ease (1948) was originally designed for English. There is a re-parameterized version for
    German, the Amstad Readability Index by Amstad (1978). However, the original version is also sometimes used to
    evaluate German texts, for example by http://www.leichtlesbar.ch. They argue, Flesch's original formula was more
    suited for the analysis of German texts, because they find Armstad's version to
    a) overestimate text difficulty at ranges of high difficulty, and
    b) be not sensitive enough to simplifications at the range of medium difficulty

    The formula is:
        206.835 - 84.6 * mean number of syllables per word - 1.015 * mean sentence length

    The index ranges between 0 and infinity, higher values indicating lower text difficulty. According to XX, average
    text difficulty is indicated by a value of XX for German and XX for English.

    :param mean_sent_length: mean sentence length in words
    :param mean_num_syllables_per_word: mean number of syllables per word
    :return: Flesch Reading Ease
    """

    return flesch_helper(206.853, 1.015 * mean_sent_length, 84.6 * mean_num_syllables_per_word)


def flesch_kincaid_grade_level(mean_sent_length, mean_num_syllables_per_word):
    """
    The Flesch-Kincaid grade level is a version of the Flesch Reading Ease scaled to school grades.

    The formula is:
        0.39 * mean sentence length + 11.8 * mean number of syllables per word - 15.9

    The index ranges between XX

    :param mean_sent_length: mean sentence length in words
    :param mean_num_syllables_per_word: mean number of syllables per word
    :return: Flesch Kincaid Grade Level
    """

    return flesch_helper(0, -0.39 * mean_sent_length, -11.8 * mean_num_syllables_per_word) - 15.59

# =====================================================================================================================
# Vienna formulae
# =====================================================================================================================


def wiener_sachtextformel_helper(param_long_syll_words, param_sent_length, param_long_char_words,
                                 param_short_syll_words, epsilon):
    """
    Helper to calculate different variants of the Wiener Sachtext formula using different parameters.

    :param param_long_syll_words: parameterized mean number of long words in terms of syllables
    :param param_sent_length: parameterized mean sentence length in words
    :param param_long_char_words: parameterized mean number of long words in terms of characters
    :param param_short_syll_words: parameterized mean number of short words in terms of syllables
    :param epsilon: epsilon parameter
    :return: Wiener Sachtext index
    """

    # compute index
    return param_long_syll_words + param_sent_length + param_long_char_words - param_short_syll_words - epsilon


def erste_wiener_sachtextformel(ratio_3_or_more_syll_words, mean_sent_length, ratio_6_or_more_char_words,
                                ratio_1_syll_words):
    """
    The first Wiener Sachtextformel

    The formula is:
        0.1935 * ratio of words with >= 3 syllables + 0.1672 * mean sentence length +
        0.1297 * ratio of words with >= 6 letters - 0.0327 * ratio of words with 1 syllable - 0.875

    :param ratio_3_or_more_syll_words: ratio of words with three or more syllables to total number of words
    :param mean_sent_length: mean sentence length in terms of words
    :param ratio_6_or_more_char_words: ratio of words with six or more letters to total number of words
    :param ratio_1_syll_words: ratio of words with one syllable to total number of words
    :return: index for first Wiener Sachtextformel
    """

    return wiener_sachtextformel_helper(0.1935 * ratio_3_or_more_syll_words, 0.1672 * mean_sent_length,
                                        0.1297 * ratio_6_or_more_char_words, 0.0327 * ratio_1_syll_words, 0.875)


def zweite_wiener_sachtextformel(ratio_3_or_more_syll_words, mean_sent_length, ratio_6_or_more_char_words):
    """
    The second Wiener Sachtextformel

    The formula is:
        0.2007 * ratio of words with >= 3 syllables + 0.1682 * mean sentence length +
        0.1373 * ratio of words with >= 6 letters - 2.779

    :param ratio_3_or_more_syll_words: ratio of words with three or more syllables to total number of words
    :param mean_sent_length: mean sentence length in terms of words
    :param ratio_6_or_more_char_words: ratio of words with six or more letters to total number of words
    :return: index for second Wiener Sachtextformel
    """

    return wiener_sachtextformel_helper(0.2007 * ratio_3_or_more_syll_words, 0.1682 * mean_sent_length,
                                        0.1373 * ratio_6_or_more_char_words, 0, 2.779)


def dritte_wiener_sachtextformel(ratio_3_or_more_syll_words, mean_sent_length):
    """
    The third Wiener Sachtextformel

    The formula is:
        0.2963 * ratio of words with >= 3 syllables + 0.1905 * mean sentence length - 1.1144

    :param ratio_3_or_more_syll_words: ratio of words with three or more syllables to total number of words
    :param mean_sent_length: mean sentence length in terms of words
    :return: index for third Wiener Sachtextformel
    """

    return wiener_sachtextformel_helper(0.2963 * ratio_3_or_more_syll_words, 0.1905 * mean_sent_length, 0, 0, 1.1144)


def vierte_wiener_sachtextformel(ratio_3_or_more_syll_words, mean_sent_length):
    """
    The fourth Wiener Sachtextformel

    The formula is:
        0.2744 * ratio of words with >= 3 syllables + 0.2656 * mean sentence length - 1.693

    :param ratio_3_or_more_syll_words: ratio of words with three or more syllables to total number of words
    :param mean_sent_length: mean sentence length in terms of words
    :return: index for third Wiener Sachtextformel
    """

    return wiener_sachtextformel_helper(0.2744 * ratio_3_or_more_syll_words, 0.2656 * mean_sent_length, 0, 0, 1.693)

# =====================================================================================================================
# Other formulae
# =====================================================================================================================


def lix_lesbarkeitsindex(mean_sent_len, ratio_long_words):
    """
    Calculates the Lix readability index
    :param mean_sent_len: mean sentence length
    :param ratio_long_words: ratio of words with six or more characters
    :return: Lix index
    """

    # compute formula
    return mean_sent_len + ratio_long_words


# def g_smog_index(num_polysyllables, num_sentences):
#     """
#
#     :param num_polysyllables: word with 3 or more syllables
#     :param num_sentences:
#     :return:
#     """
#
#     # compute formula
#     return 3.1291 if num_sentences == 0 else 1.0430 * math.sqrt(num_polysyllables * (30 / num_sentences)) + 3.1291


def gunning_fog_index(mean_sent_length, num_3_syll_words):
    """
    Calculates Gunning#s Fog index
    :param mean_sent_length: mean sentence length
    :param num_3_syll_words: average number of words with three or more syllables
    :return:
    """

    # compute formula
    return 0.4 * (mean_sent_length + num_3_syll_words)


def coleman_liau_index(word_length, sentence_word_ratio):
    """
    Calculates the Coleman Liau index
    :param word_length: average word length
    :param sentence_word_ratio: average sentence length
    :return: Coleman Liau Index
    """

    # compute formula
    return 0.0588 * word_length * 100 - 0.296 * sentence_word_ratio * 100 - 15.8


def automated_readability_index(word_length, sentence_length):
    """
    Calculates the automated readability index
    :param word_length: average word length
    :param sentence_length: average sentence length
    :return: Automated readability index
    """

    # compute formula
    return 4.71 * word_length + 0.5 * sentence_length - 21.43


# =====================================================================================================================
# L2 formulae
# =====================================================================================================================


def miyazaki_efl_readability_index(word_length, sentence_length):
    """
    Calculates the Miyazaki English as a Foreign Language Readability Index by Greenfiel 1999
    It is parametrized for Japanes L2 speakers of English, who are students and read academic texts.
    Average score of 50, ranges between 100 and minus infinity

    Formula:    164.935 - 18.792 * word_length - 1.916 * sentence_length

    :param word_length: average word length in characters
    :param sentence_length: average sentence length in words
    :return: ML2RI
    """

    return 164.935 - 18.792 * word_length - 1.916 * sentence_length
