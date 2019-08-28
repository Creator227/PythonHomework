

import argparse
import sys
from pycalc import calculator


def _args_parsing():
    """This function provides parsing command-line args using argparse module
    :returns tuple(expression, module)"""
    parser = argparse.ArgumentParser(
        'pycalc',
        description='Pure-python command-line calculator',
        usage='%(prog)s EXPRESSION [-h] [-v] [-m [MODULE [MODULE ...]]]',
        add_help=True
    )
    parser.add_argument('EXPRESSION', help='expression string to evaluate')
    parser.add_argument('-m', '--use-modules', default='',
                        help='additional modules to use', nargs='*',
                        metavar='MODULE')
    args = parser.parse_args()
    return str(args.EXPRESSION), args.use_modules


def _main():
    try:
        if len(sys.argv) == 1:
            # means, that user pressed Enter
            while True:
                expression = input(">>")
                print(calculator(expression))
        print(calculator(*_args_parsing()))
    except (ArithmeticError, ImportError) as error:
        print("ERROR:", error)
        raise SystemExit
    except (EOFError, KeyboardInterrupt):
        raise SystemExit


if __name__ == '__main__':
    _main()
