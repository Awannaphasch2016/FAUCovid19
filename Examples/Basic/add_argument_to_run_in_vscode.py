
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--something',  action='store_true',
                    help='Use GDC preprocessing.')
args = parser.parse_args()

if args.something:
    print('argument is added')
