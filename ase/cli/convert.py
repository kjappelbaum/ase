from __future__ import print_function
import os

from ase.io import read, write


class CLICommand:
    short_description = 'Convert between file formats'
    description = ('Convert between file formats.  Use "-" for stdin/stdout.  '
                   'See ase info --formats for known formats.')

    @staticmethod
    def add_arguments(parser):
        add = parser.add_argument
        add('-v', '--verbose', action='store_true',
            help='print names of converted files')
        add('input', nargs='+', metavar='input-file')
        add('-i', '--input-format', metavar='FORMAT',
            help='specify input FORMAT')
        add('output', metavar='output-file')
        add('-o', '--output-format', metavar='FORMAT',
            help='specify output FORMAT')
        add('-f', '--force', action='store_true',
            help='Overwrite an existing file')
        add('-n', '--image-number',
            default=':', metavar='NUMBER',
            help='Pick images from trajectory.  NUMBER can be a '
            'single number (use a negative number to count from '
            'the back) or a range: start:stop:step, where the '
            '":step" part can be left out - default values are '
            '0:nimages:1')

    @staticmethod
    def run(args, parser):
        if args.verbose:
            print(', '.join(args.input), '->', args.output)
        if args.arrays:
            args.arrays = [k.strip() for k in args.arrays.split(',')]
            if args.verbose:
                print('Filtering to include arrays: ', ', '.join(args.arrays))
        if args.info:
            args.info = [k.strip() for k in args.info.split(',')]
            if args.verbose:
                print('Filtering to include info: ', ', '.join(args.info))

        configs = []
        for filename in args.input:
            atoms = read(filename, args.image_number, format=args.input_format)
            if isinstance(atoms, list):
                configs.extend(atoms)
            else:
                configs.append(atoms)

        if not args.force and os.path.exists(args.output):
            parser.error('File already exists: {}'.format(args.output))

        if args.split_output:
            for i, atoms in enumerate(configs):
                write(args.output.format(i), atoms, format=args.output_format)
        else:
            write(args.output, configs, format=args.output_format)
