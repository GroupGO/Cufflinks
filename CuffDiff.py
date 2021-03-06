#!/usr/bin/env python


"""
Author: Henry Ehlers, Samin Hosseini
WUR_Number: 921013218060

A script designed to run the command line tool cuffdiff.

    Inputs:     [1] A string specifying the path to a reference annotation gtf or gff file.
                [2] A string specifying the path to the output folder.
                [3] A string specifying the overwrite option [True/False] to be used if existing
                    files or folder are encountered.
                [4] A variable number of string specifying the paths to the sorted sam files to
                    be used.

In order to provide readable and understandable code, the right indentation margin has been
increased from 79 to 99 characters, which remains in line with Python-Style-Recommendation (
https://www.python.org/dev/peps/pep-0008/) .This allows for longer, more descriptive variable
and function names, as well as more extensive doc-strings.
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
    subprocess.check_call(cmd_string, shell=True)


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


def run_cuff_diff(sorted_sam_paths, annotation, output_path, overwrite=False):
    """
    Method to run CuffDiff on the Command line.

    :param sorted_sam_paths: A list of sam file paths, one for each condition to be tested.
    :param annotation: A reference annotation gtf/gff file.
    :param output_path: The
    :return:
    """
    if not os.path.exists(output_path) or overwrite:
        print('Running Cuffdiff on {0}'.format(sorted_sam_paths))
        cmd = 'cuffdiff -p 8 -g %s -l' % annotation
        for sam_file in sorted_sam_paths:
            cmd += '%s ' % sam_file
        cmd += '-o %s' % output_path
        execute_on_command_line(cmd)
        print('Cuffdiff output saved to %s' % output_path)
    else:
        print('Directory %s already present. Not overwritten.' % output_path)


def main():
    """
    Method designed to run the command line tool cuffdiff.
    """
    annotation, output_folder_path, overwrite = get_command_line_arguments(['', '', ''])
    sorted_sam_paths = get_variable_command_line_arguments(4)
    assert os.path.exists(annotation), 'Annotation file path "%s" does not exist.' % annotation
    assert os.path.exists(output_folder_path), 'Output path "%s" not found.' % output_folder_path
    for sam_file in sorted_sam_paths:
        assert os.path.exists(sam_file), 'SAM file path "%s" no found.' % sam_file
    run_cuff_diff(sorted_sam_paths, annotation, output_folder_path, overwrite)


if __name__ == '__main__':
    main()
