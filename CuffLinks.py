#!/usr/bin/env python

"""
Author: Samin Hosseini, Henry Ehlers, Linh Nguyen

A collection of functions for the running of the Cufflinks tool on Command line.
"""


from sys import argv
import subprocess
import os.path
import re


def execute_on_command_line(cmd_string):
    """
    Method to parse a formatted string to the command line and execute it.

    :param cmd_string: The formatted string to be executed.
    """
    assert isinstance(cmd_string, str), 'Command Line String must be of type string.'
    exit_code = subprocess.check_call(cmd_string, shell=True)
    if exit_code == 1:
        exit('Critical Command Line Error: %s' % cmd_string)


def sort_sam(sam_file_name, sam_sorted):
    """

    :param sam_file_name:
    :param sam_sorted:
    :return:
    """
    if not os.path.exists(sam_sorted):
        cmd = 'samtools sort %s %s' % (sam_file_name, sam_sorted)
        execute_on_command_line(cmd)


def run_cuff_links(sam_sorted_file, reference_anotation, cufflinks_output):
    """

    :param sam_sorted_file:
    :param reference_anotation:
    :param cufflinks_output:
    :return:
    """
    if not os.path.exists(cufflinks_output):
        cmd = 'cufflinks %s -g %s -o %s' % (sam_sorted_file, reference_anotation,cufflinks_output)
        execute_on_command_line(cmd)


def run_cuff_norm(transcripts, annotation, sorted_sam_files, cuff_norm_output):
    """
    Method to run Cuffnorm on command line.

    :param transcripts:
    :param annotation:
    :param sorted_sam_files:
    :param cuff_norm_output:
    :return:
    """
    if not os.path.exists(cuff_norm_output):
        cmd = 'cuffnorm '
        for sam_file in sorted_sam_files:
            cmd += '%s ' % sam_file
        cmd += '-g %s -o %s %s' % (annotation, cuff_norm_output, transcripts)
        execute_on_command_line(cmd)


def run_cuff_quant(sam_sorted_file,  reference_anotation, cuffquant_output):
    """

    :param sam_sorted_file:
    :param reference_anotation:
    :param cuffquant_output:
    :return:
    """
    if not os.path.exists(cuffquant_output):
        cmd = 'cuffquant %s -g %s -o %s' % (sam_sorted_file, reference_anotation, cuffquant_output)
        execute_on_command_line(cmd)
    

def run_cuff_diff(sam_sorted_1, sam_sorted_2, sam_sorted_3,  reference_anotation, cuffdiff_output):
    """

    :param sam_sorted_1:
    :param sam_sorted_2:
    :param sam_sorted_3:
    :param reference_anotation:
    :param cuffdiff_output:
    :return:
    """
    if not os.path.exists(cuffdiff_output):
        cmd = 'cuffdiff -g %s -l %s %s %s -o %s'\
              % (reference_anotation, sam_sorted_1, sam_sorted_2, sam_sorted_3, cuffdiff_output)
        execute_on_command_line(cmd)


def build_name_insertion(input_names, name_insert):
    """

    :param input_names:
    :param name_insert:
    :return:
    """
    sorted_names = ['']*len(input_names)
    for index, input_name in enumerate(input_names):
        name_contents = re.split(r'\.|/', input_name)
        sorted_names[index] = ''.join(name_contents[0:-1]) + name_insert + name_contents[-1]
    return sorted_names


def extract_name_element(input_names, regex_expression, element, extension):
    """

    :param input_names:
    :param regex_expression:
    :param element:
    :param extension:
    :return:
    """
    output_names = ['']*len(input_names)
    for index, file_name in input_names:
        file_contents = re.split(regex_expression, file_name)
        output_names[index] = file_contents[element] + extension
    return output_names


def sort_all_sam_files(sam_files, sorted_sam_files):
    """

    :param sam_files:
    :param sorted_sam_files:
    :return:
    """
    for sam_name, sorted_sam_name in zip(sam_files, sorted_sam_files):
        sort_sam(sam_name, sorted_sam_name)


def run_all_cuff_links(sorted_sam_files, annotation_file, cuff_links_output):
    """

    :param sorted_sam_files:
    :param annotation_file:
    :param cuff_links_output:
    :return:
    """
    for index, sam_file in enumerate(sorted_sam_files):
        run_cuff_links(sam_file, annotation_file, cuff_links_output[index])


def run_all_cuff_norm(cuff_link_output_names, sorted_sam_files, annotation, cuff_norm_output):
    """

    :param cuff_link_output_names:
    :param sorted_sam_files:
    :param annotation:
    :param cuff_norm_output:
    :return:
    """
    for index, cuff_link_file in enumerate(cuff_link_output_names):
        run_cuff_norm(cuff_link_file, annotation, sorted_sam_files, cuff_norm_output)


def run_all_cuff_quantification(sorted_sam_files, annotation, cuff_norm_output):
    """

    :param sorted_sam_files:
    :param annotation:
    :param cuff_norm_output:
    :return:
    """
    for index, sam_file in enumerate(sorted_sam_files):
        run_cuff_quant(sam_file, annotation, cuff_norm_output)


if __name__ == "__main__":
    sam_file_names, annotation = argv[1:4], argv[4]

    sorted_sam_files = build_name_insertion(sam_file_names, '_sorted')
    sort_all_sam_files(sam_file_names, sorted_sam_files)

    cuff_links_output_names = extract_name_element(sam_file_names, r'\.|/', -2, '_cufflinks')
    run_all_cuff_links(sorted_sam_files, annotation, cuff_links_output_names)

    cuff_norm_output = extract_name_element(sam_file_names, r'\.|/', -2, '_cuffnorm')
    run_all_cuff_norm(cuff_links_output_names, sorted_sam_files, annotation, cuff_norm_output)

    cuff_norm_output = extract_name_element(sam_file_names, r'\.|/', -2, '_cuffquant')
    run_all_cuff_quantification(sorted_sam_files, annotation, cuff_norm_output)
