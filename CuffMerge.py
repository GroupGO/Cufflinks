#!/usr/bin/env python


"""
Author: Henry Ehlers, Samin Hosseini, Ronald de Jongh
WUR_Number: 921013218060, ?, 930323409080

A script designed to run the command line tool cuffdiff.

    Inputs:     [1] A string specifying the path to a Cufflinks output folder.
                [2] A string specifying the path to output folder.
                [3] A string speicyfing the overwrite option [True/False] should existing files
                    be encountered.

In order to provide readable and understandable code, the right indentation margin has been
increased from 79 to 99 characters, which remains in line with Python-Style-Recommendation (
https://www.python.org/dev/peps/pep-0008/) .This allows for longer, more descriptive variable
and function names, as well as more extensive doc-strings.

CuffMerge now checks the directories in the list itself, then appends those to the command string

"""


import subprocess
import sys
import os


def execute_on_command_line(cmd_string):
    """
    Method to parse a formatted string to the command line and execute it.

    :param cmd_string: The formatted string to be executed.
    """
    assert isinstance(cmd_string, str), 'Command Line String must be of type string.'
    exit_code = subprocess.check_call(cmd_string, shell=True)
    if exit_code == 1:
        exit('Critical Command Line Error: %s' % cmd_string)


def get_command_line_arguments(default_variable_values):
    """
    Function to get a variable number of input arguments from the command line, but use default
    values if none were given.

    :param default_variable_values: A list of default values given in order of their appearance in
    the command line.
    :return: A list of input variables.
    """
    assert isinstance(default_variable_values, list), \
        'The given default input variables values must be a list.'
    input_variables = [0]*len(default_variable_values)
    for index, default_value in enumerate(default_variable_values):
        try:
            input_variables[index] = sys.argv[index + 1]
        except IndexError:
            if default_value != '':
                input_variables[index] = default_value
            else:
                exit('Not enough command line input arguments. Critical Input Missing.')
    return input_variables


def get_variable_command_line_arguments(start_index):
    """
    Function to return a variable number of input arguments from the command line as of a
    certain index.

    :param start_index: The index of the first variable input argument on the command line.
    :return: A list of the parsed command line arguments.
    """
    variable_inputs = ['']*(len(sys.argv[:]) - start_index)
    for index, argument in enumerate(sys.argv[start_index:len(sys.argv)]):
        variable_inputs[index] = argument
    return variable_inputs


def run_cuff_merge2(manifest_path, output_path, overwrite=False):
    """
    Method to run cuff_merge on command line.

    :param manifest_path: A string specifying the path to a Cuffmerge manifest path.
    :param output_path: A string specifying the path to the output file.
    :param overwrite: A boolean specifying whether to overwrite should existing file be
    encountered.
    """
    if not os.path.exists(output_path) or overwrite:
        cmd = 'cuffmerge -o %s %s' % (output_path, manifest_path)
        execute_on_command_line(cmd)


def make_manifest_text_file(cuff_links_path, file_name):
    with open(file_name, 'w') as text_file:
        for folder in os.listdir(cuff_links_path):
            text_file.write('%s/%s/transcripts.gtf\n' % (cuff_links_path, folder))


def main():
    """
    Method designed to run the command line tool cuffmerge.
    """
    cuff_links_path, output_folder_path, run_name, overwrite = get_command_line_arguments(['']*4)
    assert os.path.exists(output_folder_path), 'Folder "%s" does not exist.' % output_folder_path
    assert os.path.exists(cuff_links_path), 'Folder "%s" does not exist.' % cuff_links_path
    manifest_name = '%s.txt' % run_name
    make_manifest_text_file(cuff_links_path, manifest_name)
    run_cuff_merge2(manifest_name, output_folder_path, overwrite)


if __name__ == '__main__':
    main()
