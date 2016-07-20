__author__ = 'zweiss'

import os
import sys

import counts as cnt
import features as feat
import readability_formulae as rf
from nlp import get_tokenized_sentences


def analyse_all_files(cur_dir, output_file, save_counts=False):
    """
    Recursively calculates readability formulae for all txt files in a given directory and all subdirectories
    :param cur_dir: directory to be analysed
    :param output_file: file where results should be saved to
    :param save_counts: saves lists of what was counted if set to true
    """

    # get a listing of all plain txt files in the dir and all sub dirs
    txt_file_list = []
    for root, dirs, files in os.walk(cur_dir):
        for name in files:
            if name.endswith('.txt'):
                txt_file_list.append(os.path.join(root, name))

    # process all files and save them to the output file
    counter = 0
    out = open(output_file, 'w')
    keys = []
    for txt_file in txt_file_list:
        print('Started analysis of ' + txt_file)

        # analyse data
        cur_formula_dict = analyse_file(txt_file, save_counts)

        # make header if necessary
        if len(keys) == 0:
            out.write('file')
            keys = sorted(cur_formula_dict.keys())
            for key in keys:
                out.write(',' + key)
            out.write('\n')

        # save data
        out.write(txt_file)
        for key in keys:
            out.write(',' + str(cur_formula_dict[key]))
        out.write('\n')

        print('Ended analysis of ' + txt_file)
        counter += 1
    out.close()
    print(str(counter) + ' file(s) processed.')
    print('Results written to ' + output_file)


def analyse_file(input_file, save_counts=False):
    """
    Calculates readability formulae for a single file
    :param input_file: input file
    :param save_counts: saves lists of what was counted if set to true
    :return: dictionary containing formulae, features and counts for the document
    """

    # get file content
    with open(input_file, 'r') as content_file:
        text = content_file.read()
    content_file.close()

    # get counts
    tokenized_sentences = get_tokenized_sentences(text)
    if save_counts:
        rval = cnt.get_and_save_counts(tokenized_sentences, input_file)
    else:
        rval = cnt.get_counts(tokenized_sentences)

    # get features
    rval.update(feat.get_features(rval))

    # get formulae
    rval.update(rf.get_formulae(rval))

    return rval


if __name__ == '__main__':

    # check for correct number of arguments
    if len(sys.argv) < 3:
        sys.exit('Wrong number of arguments, call: python3 main.py <input directory> <output file>.csv (counts)')

    # read files from directory recursively
    if len(sys.argv) == 4 and sys.argv[3].lower() == "counts":
        analyse_all_files(sys.argv[1], sys.argv[2], save_counts=True)
    else:
        analyse_all_files(sys.argv[1], sys.argv[2])

    # finished
    print('Done.')
