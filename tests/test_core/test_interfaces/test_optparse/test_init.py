#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__credits__ = ["Greg Caporaso", "Daniel McDonald", "Doug Wendel",
               "Jai Ram Rideout", "Jose Antonio Navas Molina"]

from unittest import TestCase, main
from pyqi.core.interfaces.optparse import (OptparseResult, OptparseOption,
                                           OptparseUsageExample,
                                           OptparseInterface, optparse_factory,
                                           optparse_main, PyqiOption,
                                           OptionValueError,
                                           check_existing_filepath,
                                           check_existing_filepaths,
                                           check_existing_dirpath,
                                           check_existing_dirpaths,
                                           check_new_filepath,
                                           check_new_dirpath,
                                           check_existing_path, check_new_path,
                                           check_multiple_choice,
                                           check_blast_db)
from pyqi.core.exception import IncompetentDeveloperError
from pyqi.core.command import (Command, CommandIn, CommandOut,
                               ParameterCollection, Parameter)
from tempfile import mkstemp, mkdtemp
from os import remove, rmdir
from os.path import commonprefix

class OptparseResultTests(TestCase):
    # Nothing to test yet
    pass

class OptparseOptionTests(TestCase):
    def setUp(self):
        p = CommandIn('number', int, 'some int', Required=False, Default=42,
                      DefaultDescription='forty-two')
        # With associated parameter.
        self.opt1 = OptparseOption(Parameter=p, Type=int)

        # Without associated parameter.
        self.opt2 = OptparseOption(Parameter=None, Type=int, Handler=None, 
                                   ShortName='n',
                                   Name='number', Required=False,
                                   Help='help!!!')

    def test_init(self):
        self.assertEqual(self.opt1.Type, int)
        self.assertEqual(self.opt1.Help, 'some int')
        self.assertEqual(self.opt1.Name, 'number')
        self.assertEqual(self.opt1.Default, 42)
        self.assertEqual(self.opt1.DefaultDescription, 'forty-two')
        self.assertEqual(self.opt1.ShortName, None)
        self.assertEqual(self.opt1.Required, False)

    def test_str(self):
        exp = '--number'
        obs = str(self.opt1)
        self.assertEqual(obs, exp)

        exp = '-n/--number'
        obs = str(self.opt2)
        self.assertEqual(obs, exp)

class OptparseUsageExampleTests(TestCase):
    def test_init(self):
        obj = OptparseUsageExample(ShortDesc='a', LongDesc='b', Ex='c')
        self.assertEqual(obj.ShortDesc, 'a')
        self.assertEqual(obj.LongDesc, 'b')
        self.assertEqual(obj.Ex, 'c')

        with self.assertRaises(IncompetentDeveloperError):
            _ = OptparseUsageExample('a', 'b', Ex=None)

def oh(key, data, opt_value=None):
    return data * 2

class OptparseInterfaceTests(TestCase):
    def setUp(self):
        self.interface = fabulous()
    
    def test_init(self):
        self.assertRaises(IncompetentDeveloperError, OptparseInterface)

    def test_validate_usage_examples(self):
        with self.assertRaises(IncompetentDeveloperError):
            _ = NoUsageExamples()

    # TODO: this test should be migrated to tests for the Interface baseclass
    # if/when they exist.
    def test_validate_inputs(self):
        with self.assertRaises(IncompetentDeveloperError):
            _ = DuplicateOptionMappings()

    def test_input_handler(self):
        obs = self.interface._input_handler(['--c','foo'])
        self.assertEqual(list(obs.items()), [('c', 'foo')])

    def test_build_usage_lines(self):
        obs = self.interface._build_usage_lines([])
        self.assertEqual(obs, usage_lines)

    def test_output_handler(self):
        results = {'itsaresult':20}
        obs = self.interface._output_handler(results)
        self.assertEqual(obs, {'itsaresult':40})

class GeneralTests(TestCase):
    def setUp(self):
        self.obj = optparse_factory(ghetto,
                [OptparseUsageExample('a','b','c')],
                [OptparseOption(Type=str,
                                Parameter=ghetto.CommandIns['c'],
                                ShortName='n')],
                [OptparseResult(Type=str,
                                Parameter=ghetto.CommandOuts['itsaresult'],
                                Handler=oh)],
                '2.0-dev')

    def test_optparse_factory(self):
        # exercise it
        _ = self.obj()

    def test_optparse_main(self):
        # exercise it
        _ = optparse_main(self.obj, ['testing', '--c', 'bar'])

class ghetto(Command):
    CommandIns = ParameterCollection([CommandIn('c', str, 'b')])
    CommandOuts = ParameterCollection([CommandOut('itsaresult', str, 'x')])

    def run(self, **kwargs):
        return {'itsaresult':10}

class fabulous(OptparseInterface):
    CommandConstructor = ghetto

    def _get_inputs(self):
        return [OptparseOption(Type=str,
                Parameter=self.CommandConstructor.CommandIns['c'],
                ShortName='n')]

    def _get_usage_examples(self):
        return [OptparseUsageExample('a','b','c')]

    def _get_outputs(self):
        return [OptparseResult(Parameter=ghetto.CommandOuts['itsaresult'], Handler=oh)]

    def _get_version(self):
        return '2.0-dev'

# Doesn't have any usage examples...
class NoUsageExamples(fabulous):
    def _get_usage_examples(self):
        return []

# More than one option mapping to the same Parameter...
class DuplicateOptionMappings(fabulous):
    def _get_inputs(self):
        return [
            OptparseOption(Type=str,
            Parameter=self.CommandConstructor.CommandIns['c'], ShortName='n'),

            OptparseOption(Parameter=self.CommandConstructor.CommandIns['c'],
            Name='i-am-a-duplicate')
        ]

class TypeCheckTests(TestCase):
    def setUp(self):
        self._paths_to_clean_up = []
        self._dirs_to_clean_up = []

    def tearDown(self):
        for p in self._paths_to_clean_up:
            remove(p)
        for d in self._dirs_to_clean_up:
            rmdir(d)

    def test_check_existing_filepath(self):
        # Check that returns the correct value when the file exists
        tmp_f, tmp_path = mkstemp()
        self._paths_to_clean_up = [tmp_path]
        option = PyqiOption('-f', '--file_test', type='existing_filepath')
        obs = check_existing_filepath(option, '-f', tmp_path)
        self.assertEqual(obs, tmp_path)
        # Check that raises an error when the file doesn't exists
        self.assertRaises(OptionValueError, check_existing_filepath, option,
            '-f', '/hopefully/a/non/existing/file')
        # Check that raises an error when the path exists and is a directory
        tmp_dirpath = mkdtemp()
        self._dirs_to_clean_up = [tmp_dirpath]
        self.assertRaises(OptionValueError, check_existing_filepath, option,
            '-f', tmp_dirpath)

    def test_check_existing_filepaths(self):
        # Check that returns a list with the paths, in the same order as 
        # the input comma separated list
        tmp_f1, tmp_path1 = mkstemp(prefix='pyqi_tmp_testf')
        tmp_f2, tmp_path2 = mkstemp(prefix='pyqi_tmp_testf')
        self._paths_to_clean_up = [tmp_path1, tmp_path2]
        option = PyqiOption('-f', '--files_test', type='existing_filepaths')
        exp = [tmp_path1, tmp_path2]
        value = ",".join(exp)
        obs = check_existing_filepaths(option, '-f', value)
        self.assertEqual(obs, exp)
        # Check that returns a list with the paths when using wildcards
        # note that the order is not important now
        value = commonprefix(exp) + '*'
        obs = check_existing_filepaths(option, '-f', value)
        self.assertEqual(set(obs), set(exp))
        # Check that raises an error when the wildcard does not match any file
        self.assertRaises(OptionValueError, check_existing_filepaths, option,
            '-f', '/hopefully/a/non/existing/path*')
        # Check that raises an error when one of the files does not exist
        value = ",".join([tmp_path1,tmp_path2,'/hopefully/a/non/existing/file'])
        self.assertRaises(OptionValueError, check_existing_filepaths, option,
            '-f', value)
        # Check that raises an error when one of the paths is a folder
        tmp_dirpath = mkdtemp()
        self._dirs_to_clean_up = [tmp_dirpath]
        value = ",".join([tmp_path1, tmp_path2, tmp_dirpath])
        self.assertRaises(OptionValueError, check_existing_filepaths, option,
            '-f', value)

    def test_check_existing_dirpath(self):
        # Check that returns the correct value when the directory exists
        tmp_dirpath = mkdtemp()
        self._dirs_to_clean_up = [tmp_dirpath]
        option = PyqiOption('-d', '--dir_test', type='existing_dirpath')
        obs = check_existing_dirpath(option, '-d', tmp_dirpath)
        self.assertEqual(obs, tmp_dirpath)
        # Check that raises an error when the folder doesn't exists
        self.assertRaises(OptionValueError, check_existing_dirpath, option,
            '-f', '/hopefully/a/non/existing/directory')
        # Check that raises an error when the path exists and is a file
        tmp_f, tmp_path = mkstemp()
        self._paths_to_clean_up = [tmp_path]
        self.assertRaises(OptionValueError, check_existing_dirpath, option,
            '-f', tmp_path)

    def test_check_existing_dirpaths(self):
        # Check that returns a list with the paths, in the same order as the
        # input comma separated list
        tmp_dirpath1 = mkdtemp(prefix='pyqi_tmp_testd_')
        tmp_dirpath2 = mkdtemp(prefix='pyqi_tmp_testd_')
        self._dirs_to_clean_up = [tmp_dirpath1, tmp_dirpath2]
        option = PyqiOption('-d', '--dirs_test', type='existing_dirpaths')
        exp = [tmp_dirpath1, tmp_dirpath2]
        value = ",".join(exp)
        obs = check_existing_dirpaths(option, '-d', value)
        self.assertEqual(obs, exp)
        # Check that returns a list with the paths when using wildcars
        # note that the order is not important now
        value = commonprefix(exp) + '*'
        obs = check_existing_dirpaths(option, '-d', value)
        self.assertEqual(set(obs), set(exp))
        # Check that raises an error when the wildcard does not match any path
        self.assertRaises(OptionValueError, check_existing_dirpaths, option,
            '-f', '/hopefully/a/non/existing/path*')
        # Check that raises an error when one of the directories does not exist
        value = ",".join([tmp_dirpath1, tmp_dirpath2,
            '/hopefully/a/non/existing/path*'])
        self.assertRaises(OptionValueError, check_existing_dirpaths, option,
            '-f', value)
        # Check that raises an error when one of the paths is a file
        tmp_f, tmp_path = mkstemp()
        self._paths_to_clean_up = [tmp_path]
        value = ",".join([tmp_dirpath1, tmp_dirpath2, tmp_path])
        self.assertRaises(OptionValueError, check_existing_dirpaths, option,
            '-f', value)

    def test_check_new_filepath(self):
        # Check that it doesn't raise an error if the path does not exist
        option = PyqiOption('-n', '--new_file', type="new_filepath")
        exp = '/hopefully/a/non/existing/file'
        obs = check_new_filepath(option, '-n', exp)
        self.assertEqual(obs, exp)
        # Check that it doesn't raise an error if the path exists and is a file
        tmp_f, tmp_path = mkstemp()
        self._paths_to_clean_up = [tmp_path]
        obs = check_new_filepath(option, '-n', tmp_path)
        self.assertEqual(obs, tmp_path)
        # Check that it raises an error if the path exist and is a directory
        tmp_dirpath = mkdtemp()
        self._dirs_to_clean_up = [tmp_dirpath]
        self.assertRaises(OptionValueError, check_new_filepath, option, '-n',
            tmp_dirpath)

    def test_check_new_dirpath(self):
        # Check that it doesn't raise an error if the path does not exist
        option = PyqiOption('-n', '--new_dir', type='new_dirpath')
        exp = '/hopefully/a/non/existing/dir'
        obs = check_new_dirpath(option, '-n', exp)
        self.assertEqual(obs, exp)
        # Check that it doesn't raise an error if the path exists and is a directory
        tmp_dirpath = mkdtemp()
        self._dirs_to_clean_up = [tmp_dirpath]
        obs = check_new_dirpath(option, '-n', tmp_dirpath)
        self.assertEqual(obs, tmp_dirpath)
        # Check that it raises an error if the path exists and is a file
        tmp_f, tmp_path = mkstemp()
        self._paths_to_clean_up = [tmp_path]
        self.assertRaises(OptionValueError, check_new_dirpath, option, '-n',
            tmp_path)

    def test_check_existing_path(self):
        # Check that it doesn't raise an error if an existing file is passed
        option = PyqiOption('-p', '--path_test', type='existing_path')
        tmp_f, tmp_path = mkstemp()
        self._paths_to_clean_up = [tmp_path]
        obs = check_existing_path(option, '-p', tmp_path)
        self.assertEqual(obs, tmp_path)
        # Check that it doesn't raise an error if an existing directory is passed
        tmp_dirpath = mkdtemp()
        self._dirs_to_clean_up = [tmp_dirpath]
        obs = check_existing_path(option, '-p', tmp_dirpath)
        self.assertEqual(obs, tmp_dirpath)
        # Check that it raises an error if the path doesn't exist
        self.assertRaises(OptionValueError, check_existing_path, option, '-n',
            '/hopefully/a/non/existing/path')

    def test_check_new_path(self):
        # Really? Too much work...
        option = PyqiOption('-n', '--new_path', type="new_path")
        exp = '/nothing/to/test/here'
        obs = check_new_path(option, '-n', exp)
        self.assertEqual(obs, exp)

    def test_check_multiple_choice(self):
        # Check that it doesn't raise an error when the value is in the list
        option = PyqiOption('-m', '--multiple', type="multiple_choice",
            mchoices=['choice_A', 'choice_B', 'choice_C'])
        exp = ["choice_B"]
        obs = check_multiple_choice(option, '-m', exp[0])
        self.assertEqual(obs, exp)
        exp = ["choice_B","choice_C"]
        obs = check_multiple_choice(option, '-m', ",".join(exp))
        self.assertEqual(obs, exp)
        # Check that it raises an error when the value is not in the list
        self.assertRaises(OptionValueError, check_multiple_choice, option, '-n',
            "choice_not_listed")
        self.assertRaises(OptionValueError, check_multiple_choice, option, '-n',
            "choice_A,choice_not_listed")

    def test_check_blast_db(self):
        # Check that it doesn't raise an error when a blastdb-like prefix is passed
        option = PyqiOption('-b', '--blast_test', type="blast_db")
        tmp_f1, tmp_path1 = mkstemp(prefix='pyqi_tmp_')
        tmp_f2, tmp_path2 = mkstemp(prefix='pyqi_tmp_')
        self._paths_to_clean_up = [tmp_path1, tmp_path2]
        exp = commonprefix([tmp_path1, tmp_path2])
        obs = check_blast_db(option, '-b', exp)
        self.assertEqual(obs, exp)
        # Check that raises an error if the base folder does not exist
        self.assertRaises(OptionValueError, check_blast_db, option, '-b',
            '/hopefully/a/non/existing/path')

usage_lines = """usage: %prog [options] {}

[] indicates optional input (order unimportant)
{} indicates required input (order unimportant)



Example usage: 
Print help message and exit
 %prog -h

a: b
 c"""


if __name__ == '__main__':
    main()
