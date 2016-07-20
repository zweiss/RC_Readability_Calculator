__author__ = 'zweiss'


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from readability_formulae import *
from scipy import stats
from sklearn.dummy import DummyClassifier

from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import StratifiedKFold, cross_val_score


def plot_felsch_scores(sentence_length, word_length, var_asl=True):
    """
    Plots all three Flesch scores
    :param sentence_length: average sentence length
    :param word_length: average word length
    :param var_asl: True if sentence length is variable and word length is fixed, false otherwise
    """

    if var_asl:
        x = sentence_length
        xlabel = 'Average Sentence Length in Tokens'
    else:
        x = word_length
        xlabel = 'Average Word Length in Syllables'

    plt.plot(x, amstad_lesbarkeits_index(sentence_length, word_length), color="blue", label="Amstad Readability Index")
    plt.plot(x, flesch_reading_ease(sentence_length, word_length), color="red", label="Flesch Reading Ease")
    plt.plot(x, flesch_kincaid_grade_level(sentence_length, word_length), color="green", label="Flesch Grade Score")
    plt.legend(loc='best')
    plt.ylabel('Readability Score')
    plt.xlabel(xlabel)
    plt.show()


def plot_vienna_scores(long_words_syll, sent_length, long_words_char, short_words_syll, var_long_syll=True):
    """
    Plots all four Wiener Sachlichkeitsformeln
    :param long_words_syll: average number of long syllable words
    :param sent_length: average sentence length
    :param long_words_char: average number of long character words
    :param short_words_syll: average number of short syllable words
    :param var_long_Syll: true if number of long syllable words is variable, false if sentence length is
    """

    if var_long_syll:
        x = long_words_syll
        xlabel = 'Ratio of Words >= 3 Syllables'
    else:
        x = sent_length
        xlabel = 'Average Sentence Length in Tokens'

    plt.plot(x, erste_wiener_sachtextformel(long_words_syll, sent_length, long_words_char, short_words_syll),
             color="blue", label="1st WSF")
    plt.plot(x, zweite_wiener_sachtextformel(long_words_syll, sent_length, long_words_char), color="red",
             label="2nd WSF")
    plt.plot(x, dritte_wiener_sachtextformel(long_words_syll, sent_length), color="green", label="3rd WSF")
    plt.plot(x, vierte_wiener_sachtextformel(long_words_syll, sent_length), color="orange", label="4th WSF")
    plt.legend(loc='best')
    plt.ylabel('Readability Score')
    plt.xlabel(xlabel)
    plt.show()


if __name__ == '__main__':

    np.random.seed(1)

    # =================================================================================================================
    # I. Make plots to identify the effect of different features
    # =================================================================================================================

    Avg_Sent_Len = np.linspace(5, 35, 30, endpoint=False)
    Avg_Word_Len = np.linspace(1, 3, 5, endpoint=False)
    Long_Syll_Words = np.linspace(0, 1, 10, endpoint=False)

    # plot Flesch scores for varying sentence lengths and word lengths
    plot_felsch_scores(Avg_Sent_Len, 2, var_asl=True)
    plot_felsch_scores(5, Avg_Word_Len, var_asl=False)

    # plot Wiener Sachtextformeln for varying word and sentence lengths
    plot_vienna_scores(.3, Avg_Sent_Len, .3, .6, var_long_syll=False)
    plot_vienna_scores(Long_Syll_Words, 5, .3, .6, var_long_syll=True)

    # =================================================================================================================
    # II. Identify min and max values for each formual
    # =================================================================================================================

    # get min and max values for Flesch
    formula = ['FRE', 'FGL', 'ALI', 'WSF1', 'WSF2', 'WSF3', 'WSF4', 'LIX', 'MELFRI', 'GFI', 'CLI', 'ARI']
    lower = [flesch_reading_ease(1, 0), flesch_kincaid_grade_level(1, 0), amstad_lesbarkeits_index(1, 0),
             erste_wiener_sachtextformel(0, 1, 0, 1), zweite_wiener_sachtextformel(0, 1, 0),
             dritte_wiener_sachtextformel(0, 1), vierte_wiener_sachtextformel(0, 1), lix_lesbarkeitsindex(1, 0),
             miyazaki_efl_readability_index(1, 1), gunning_fog_index(1, 0), coleman_liau_index(1,1),
             automated_readability_index(1, 1)]
    upper = [flesch_reading_ease(100000, 100000), flesch_kincaid_grade_level(100000, 100000),
             amstad_lesbarkeits_index(100000, 100000), erste_wiener_sachtextformel(100000, 100000, 100000, 100000),
             zweite_wiener_sachtextformel(100000, 100000, 100000), dritte_wiener_sachtextformel(100000, 100000),
             vierte_wiener_sachtextformel(100000, 100000), lix_lesbarkeitsindex(100000, 100000),
             miyazaki_efl_readability_index(100000, 100000), gunning_fog_index(100000, 100000), coleman_liau_index(100000,100000),
             automated_readability_index(100000, 100000)]
    boundaries = pd.DataFrame({'Min': lower, 'Max': upper}, index=formula)
    print(boundaries)


    # =================================================================================================================
    # III. Perform multinomial logistic regression with data
    # =================================================================================================================

    input_dir = '/Users/zweiss/Documents/Uni/9_SS16/nltk_project-ws1516/ml-analysis/merlin-readability_formulas-160714_meta.csv'
    data_raw = pd.read_csv(input_dir)
    data = data_raw[data_raw.CERF_OverallScore != 'C2']  # drop C2 level (not enough instances for 10-folds cv)
    data.head()
    data.shape
    data.columns

    classes = data.iloc[:, 6].as_matrix()  # cerf overall score at index 6
    classes

    folds = StratifiedKFold(classes, 10)  # creates an index to be used in cross validation

    lr = LogisticRegression(multi_class='multinomial', solver='lbfgs')

    # iterate over features and build models based on single fomula
    lr_f1 = []
    lr_precision = []
    lr_recall = []

    start_formluae = 31  # formulae start at index 31
    for f in range(start_formluae, len(data.columns)):
        predictors = data.iloc[:, [f]].values
        lr_f1.append(cross_val_score(lr, predictors, classes, cv=10, scoring='f1_weighted'))
        lr_precision.append(cross_val_score(lr, predictors, classes, cv=10, scoring='precision_weighted'))
        lr_recall.append(cross_val_score(lr, predictors, classes, cv=10, scoring='recall_weighted'))
        # _micro, _macro, _weighted, _samples

    # feature baseline
    feat_f1 = cross_val_score(lr, data.iloc[:, 23:start_formluae].values, classes, cv=10, scoring='f1_weighted')
    feat_precision = cross_val_score(lr, data.iloc[:, 23:start_formluae].values, classes, cv=10, scoring='precision_weighted')
    feat_recall = cross_val_score(lr, data.iloc[:, 23:start_formluae].values, classes, cv=10, scoring='recall_weighted')

    # majority baseline
    dummy_classifier = DummyClassifier(strategy="most_frequent", random_state=0)
    random_f1 = cross_val_score(dummy_classifier, [[0]]*len(classes), classes, cv=10, scoring='f1_weighted')
    random_precision = cross_val_score(dummy_classifier, [[0]]*len(classes), classes, cv=10, scoring='precision_weighted')
    random_recall = cross_val_score(dummy_classifier, [[0]]*len(classes), classes, cv=10, scoring='recall_weighted')

    f1_performance = pd.DataFrame({'ALI': lr_f1[0], 'FGS': lr_f1[1], 'FRE': lr_f1[2], 'MRI': lr_f1[3], 'ARI': lr_f1[4],
                                   'CLI': lr_f1[5], 'Fog': lr_f1[6], 'Lix': lr_f1[7], 'WSF1': lr_f1[8], 'WSF2': lr_f1[9],
                                   'WSF3': lr_f1[10], 'WSF4': lr_f1[11], 'FEAT': feat_f1, 'BASE': random_f1},
                                  index=[n for n in range(0, 10)])
    f1_performance.mean()

    precision_performance = pd.DataFrame({'ALI': lr_precision[0], 'FGS': lr_precision[1], 'FRE': lr_precision[2],
                                          'MRI': lr_precision[3], 'ARI': lr_precision[4], 'CLI': lr_precision[5],
                                          'Fog': lr_precision[6], 'Lix': lr_precision[7], 'WSF1': lr_precision[8],
                                          'WSF2': lr_precision[9], 'WSF3': lr_precision[10], 'WSF4': lr_precision[11],
                                          'FEAT': feat_precision, 'BASE': random_precision},
                                         index=[n for n in range(0, 10)])
    precision_performance.mean()

    recall_performance = pd.DataFrame({'ALI': lr_recall[0], 'FGS': lr_recall[1], 'FRE': lr_recall[2],
                                       'MRI': lr_recall[3], 'ARI': lr_recall[4], 'CLI': lr_recall[5],
                                       'Fog': lr_recall[6], 'Lix': lr_recall[7], 'WSF1': lr_recall[8],
                                       'WSF2': lr_recall[9], 'WSF3': lr_recall[10], 'WSF4': lr_recall[11],
                                       'FEAT': feat_recall, 'BASE': random_recall},
                                      index=[n for n in range(0, 10)])
    recall_performance.mean()

    # ================================================================================================================

    # compare f1 to random baseline
    stats.ttest_rel(f1_performance.BASE, f1_performance.FEAT)  # significant for a = .01
    stats.ttest_rel(f1_performance.BASE, f1_performance.CLI)  # significant for a = .01
    stats.ttest_rel(f1_performance.BASE, f1_performance.Fog)  # significant for a = .01
    stats.ttest_rel(f1_performance.BASE, f1_performance.WSF3)  # significant for a = .01
    stats.ttest_rel(f1_performance.BASE, f1_performance.WSF4)  # significant for a = .01
    stats.ttest_rel(f1_performance.BASE, f1_performance.Lix)  # significant for a = .01
    stats.ttest_rel(f1_performance.BASE, f1_performance.WSF2)  # significant for a = .01
    stats.ttest_rel(f1_performance.BASE, f1_performance.WSF1)  # significant for a = .01
    stats.ttest_rel(f1_performance.BASE, f1_performance.FGS)  # significant for a = .01
    stats.ttest_rel(f1_performance.BASE, f1_performance.MRI)  # significant for a = .01
    stats.ttest_rel(f1_performance.BASE, f1_performance.ARI)  # significant for a = .01
    stats.ttest_rel(f1_performance.BASE, f1_performance.ALI)  # significant for a = .01
    stats.ttest_rel(f1_performance.BASE, f1_performance.FRE)  # significant for a = .01

    # compare precision to random baseline
    stats.ttest_rel(precision_performance.BASE, precision_performance.FEAT)  # significant for a = .01
    stats.ttest_rel(precision_performance.BASE, precision_performance.CLI)  # significant for a = .01
    stats.ttest_rel(precision_performance.BASE, precision_performance.Fog)  # significant for a = .01
    stats.ttest_rel(precision_performance.BASE, precision_performance.WSF3)  # significant for a = .01
    stats.ttest_rel(precision_performance.BASE, precision_performance.WSF4)  # significant for a = .01
    stats.ttest_rel(precision_performance.BASE, precision_performance.Lix)  # significant for a = .01
    stats.ttest_rel(precision_performance.BASE, precision_performance.WSF2)  # significant for a = .01
    stats.ttest_rel(precision_performance.BASE, precision_performance.WSF1)  # significant for a = .01
    stats.ttest_rel(precision_performance.BASE, precision_performance.FGS)  # significant for a = .01
    stats.ttest_rel(precision_performance.BASE, precision_performance.MRI)  # significant for a = .01
    stats.ttest_rel(precision_performance.BASE, precision_performance.ARI)  # significant for a = .01
    stats.ttest_rel(precision_performance.BASE, precision_performance.ALI)  # significant for a = .01
    stats.ttest_rel(precision_performance.BASE, precision_performance.FRE)  # significant for a = .01

    # compare recall to random baseline
    stats.ttest_rel(recall_performance.BASE, recall_performance.FEAT)  # significant for a = .01
    stats.ttest_rel(recall_performance.BASE, recall_performance.CLI)  # significant for a = .01
    stats.ttest_rel(recall_performance.BASE, recall_performance.Fog)  # significant for a = .01
    stats.ttest_rel(recall_performance.BASE, recall_performance.WSF3)  # significant for a = .01
    stats.ttest_rel(recall_performance.BASE, recall_performance.WSF4)  # significant for a = .01
    stats.ttest_rel(recall_performance.BASE, recall_performance.Lix)  # significant for a = .01
    stats.ttest_rel(recall_performance.BASE, recall_performance.WSF2)  # significant for a = .01
    stats.ttest_rel(recall_performance.BASE, recall_performance.WSF1)  # significant for a = .01
    stats.ttest_rel(recall_performance.BASE, recall_performance.FGS)  # significant for a = .01
    stats.ttest_rel(recall_performance.BASE, recall_performance.MRI)  # significant for a = .01
    stats.ttest_rel(recall_performance.BASE, recall_performance.ARI)  # significant for a = .01
    stats.ttest_rel(recall_performance.BASE, recall_performance.ALI)  # significant for a = .01
    stats.ttest_rel(recall_performance.BASE, recall_performance.FRE)  # significant for a = .01

    # ================================================================================================================

    # compare f1 to feature baseline
    stats.ttest_rel(f1_performance.FEAT, f1_performance.BASE)  # significant for a = .01
    stats.ttest_rel(f1_performance.FEAT, f1_performance.CLI)  # significant for a = .01
    stats.ttest_rel(f1_performance.FEAT, f1_performance.Fog)  # significant for a = .05
    stats.ttest_rel(f1_performance.FEAT, f1_performance.WSF3)  # significant for a = .05
    stats.ttest_rel(f1_performance.FEAT, f1_performance.WSF4)  # significant for a = .05
    stats.ttest_rel(f1_performance.FEAT, f1_performance.Lix)  # significant for a = .05
    stats.ttest_rel(f1_performance.FEAT, f1_performance.WSF2)  # significant for a = .05
    stats.ttest_rel(f1_performance.FEAT, f1_performance.WSF1)  # significant for a = .05
    stats.ttest_rel(f1_performance.FEAT, f1_performance.FGS)
    stats.ttest_rel(f1_performance.FEAT, f1_performance.MRI)
    stats.ttest_rel(f1_performance.FEAT, f1_performance.ARI)
    stats.ttest_rel(f1_performance.FEAT, f1_performance.ALI)
    stats.ttest_rel(f1_performance.FEAT, f1_performance.FRE)

    # compare precision to feature baseline
    stats.ttest_rel(precision_performance.FEAT, precision_performance.BASE)  # significant for a = .01
    stats.ttest_rel(precision_performance.FEAT, precision_performance.CLI)  # significant for a = .01
    stats.ttest_rel(precision_performance.FEAT, precision_performance.Fog)  # significant for a = .05
    stats.ttest_rel(precision_performance.FEAT, precision_performance.WSF3)  # significant for a = .05
    stats.ttest_rel(precision_performance.FEAT, precision_performance.WSF4)  # significant for a = .01
    stats.ttest_rel(precision_performance.FEAT, precision_performance.Lix)  # significant for a = .05
    stats.ttest_rel(precision_performance.FEAT, precision_performance.WSF2)  # significant for a = .05
    stats.ttest_rel(precision_performance.FEAT, precision_performance.WSF1)  # significant for a = .05
    stats.ttest_rel(precision_performance.FEAT, precision_performance.FGS)
    stats.ttest_rel(precision_performance.FEAT, precision_performance.MRI)
    stats.ttest_rel(precision_performance.FEAT, precision_performance.ARI)
    stats.ttest_rel(precision_performance.FEAT, precision_performance.ALI)
    stats.ttest_rel(precision_performance.FEAT, precision_performance.FRE)

    # compare recall to feature baseline
    stats.ttest_rel(recall_performance.FEAT, recall_performance.BASE)  # significant for a = .01
    stats.ttest_rel(recall_performance.FEAT, recall_performance.CLI)  # significant for a = .01
    stats.ttest_rel(recall_performance.FEAT, recall_performance.Fog)  # significant for a = .01
    stats.ttest_rel(recall_performance.FEAT, recall_performance.WSF3)  # significant for a = .01
    stats.ttest_rel(recall_performance.FEAT, recall_performance.WSF4)  # significant for a = .01
    stats.ttest_rel(recall_performance.FEAT, recall_performance.Lix)  # significant for a = .01
    stats.ttest_rel(recall_performance.FEAT, recall_performance.WSF2)  # significant for a = .01
    stats.ttest_rel(recall_performance.FEAT, recall_performance.WSF1)  # significant for a = .01
    stats.ttest_rel(recall_performance.FEAT, recall_performance.FGS)
    stats.ttest_rel(recall_performance.FEAT, recall_performance.MRI)
    stats.ttest_rel(recall_performance.FEAT, recall_performance.ARI)
    stats.ttest_rel(recall_performance.FEAT, recall_performance.ALI)
    stats.ttest_rel(recall_performance.FEAT, recall_performance.FRE)

    # ================================================================================================================

    # compare f1 to best model (based on f1 score)
    stats.ttest_rel(f1_performance.CLI, f1_performance.FEAT)  # significant for a = .01
    stats.ttest_rel(f1_performance.CLI, f1_performance.Fog)  # significant for a = .01
    stats.ttest_rel(f1_performance.CLI, f1_performance.WSF3)  # significant for a = .01
    stats.ttest_rel(f1_performance.CLI, f1_performance.Lix)  # significant for a = .01
    stats.ttest_rel(f1_performance.CLI, f1_performance.WSF2)  # significant for a = .01
    stats.ttest_rel(f1_performance.CLI, f1_performance.WSF1)  # significant for a = .01
    stats.ttest_rel(f1_performance.CLI, f1_performance.WSF4)  # significant for a = .01
    stats.ttest_rel(f1_performance.CLI, f1_performance.FGS)
    stats.ttest_rel(f1_performance.CLI, f1_performance.MRI)
    stats.ttest_rel(f1_performance.CLI, f1_performance.ARI)
    stats.ttest_rel(f1_performance.CLI, f1_performance.ALI)
    stats.ttest_rel(f1_performance.CLI, f1_performance.FRE)

    # compare precision to best model (based on f1 score)
    stats.ttest_rel(precision_performance.CLI, precision_performance.FEAT)  # significant for a = .01
    stats.ttest_rel(precision_performance.CLI, precision_performance.Fog)  # significant for a = .01
    stats.ttest_rel(precision_performance.CLI, precision_performance.WSF3)  # significant for a = .01
    stats.ttest_rel(precision_performance.CLI, precision_performance.Lix)  # significant for a = .01
    stats.ttest_rel(precision_performance.CLI, precision_performance.WSF2)  # significant for a = .01
    stats.ttest_rel(precision_performance.CLI, precision_performance.WSF1)  # significant for a = .01
    stats.ttest_rel(precision_performance.CLI, precision_performance.WSF4)  # significant for a = .01
    stats.ttest_rel(precision_performance.CLI, precision_performance.FGS)
    stats.ttest_rel(precision_performance.CLI, precision_performance.MRI)
    stats.ttest_rel(precision_performance.CLI, precision_performance.ARI)
    stats.ttest_rel(precision_performance.CLI, precision_performance.ALI)
    stats.ttest_rel(precision_performance.CLI, precision_performance.FRE)

    # compare recall to best model (based on f1 score)
    stats.ttest_rel(recall_performance.CLI, recall_performance.FEAT)  # significant for a = .01
    stats.ttest_rel(recall_performance.CLI, recall_performance.Fog)  # significant for a = .01
    stats.ttest_rel(recall_performance.CLI, recall_performance.WSF3)  # significant for a = .01
    stats.ttest_rel(recall_performance.CLI, recall_performance.Lix)  # significant for a = .01
    stats.ttest_rel(recall_performance.CLI, recall_performance.WSF2)  # significant for a = .01
    stats.ttest_rel(recall_performance.CLI, recall_performance.WSF1)  # significant for a = .01
    stats.ttest_rel(recall_performance.CLI, recall_performance.WSF4)  # significant for a = .01
    stats.ttest_rel(recall_performance.CLI, recall_performance.FGS)
    stats.ttest_rel(recall_performance.CLI, recall_performance.MRI)
    stats.ttest_rel(recall_performance.CLI, recall_performance.ARI)
    stats.ttest_rel(recall_performance.CLI, recall_performance.ALI)
    stats.ttest_rel(recall_performance.CLI, recall_performance.FRE)

    # compare WSF with each other
    stats.ttest_rel(f1_performance.WSF1, f1_performance.WSF2)
    stats.ttest_rel(f1_performance.WSF1, f1_performance.WSF3)
    stats.ttest_rel(f1_performance.WSF1, f1_performance.WSF4)  # significant for a = .05
    stats.ttest_rel(f1_performance.WSF2, f1_performance.WSF3)
    stats.ttest_rel(f1_performance.WSF2, f1_performance.WSF4)  # significant for a = .05
    stats.ttest_rel(f1_performance.WSF3, f1_performance.WSF4)  # significant for a = .05

    # compare Flesch formulae with each other
    stats.ttest_rel(f1_performance.ALI, f1_performance.FRE)
    stats.ttest_rel(f1_performance.ALI, f1_performance.FGS)
    stats.ttest_rel(f1_performance.FGS, f1_performance.FRE)
