from qcli.interface.cli import CLOption, UsageExample, ParameterConversion
from qcli.qcli_command.make_command import CommandConstructor

usage_examples = [
        UsageExample(ShortDesc="Basic function",
                     LongDesc="Create a basic function with appropriate attribution",
                     Ex='%prog -n example -a "some author" -c "Copyright 2013, The QCLI Project" -e "foo@bar.com" -l BSD --func_version "0.1" --credits "someone else","and another person" -o example.py')
        ]

param_conversions = {
        'name':ParameterConversion(ShortName='n',
                                     LongName='name',
                                     CLType=str),
        'email':ParameterConversion(ShortName='e',
                                     LongName='email',
                                     CLType=str),
        'author':ParameterConversion(ShortName='a',
                                     LongName='author',
                                     CLType=str),
        'license':ParameterConversion(ShortName='l',
                                     LongName='license',
                                     CLType=str),
        'copyright':ParameterConversion(ShortName='c',
                                     LongName='copyright',
                                     CLType=str),
        'credits':ParameterConversion(ShortName=None,
                                     LongName='credits',
                                     CLType=str),
        'func_version':ParameterConversion(ShortName=None,
                                     LongName='func_version',
                                     CLType=str),
        }

additional_options = [
        CLOption(Type='output_file',
                 Help='the resulting Python file',
                 Name='output_fp',
                 Required=True,
                 LongName='output-fp',
                 CLType='new_filepath',
                 ShortName='o',
                 ResultName='result')
        ]
