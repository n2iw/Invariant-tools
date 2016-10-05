#!/usr/local/bin/python3
import os, sys
import argparse

PREFIX = os.environ['PWD']

def main():
    parser = argparse.ArgumentParser(description="Compute invariant violations")

    # run in folder
    parser.add_argument('--prefix', help="parent folder of all fixed and buggy folders" ,
            default=PREFIX)
    # version range
    parser.add_argument('fixed',  help='base invariant file')
    parser.add_argument('buggies', nargs='+', help='buggy invariant files')
    parser.add_argument('-d', '--dry-run', help="only print commands, won't run it" , action='store_true')

    args = parser.parse_args()

    for f in args.buggies:

        cmd = 'invViolates.py {} {} > {}'.format(args.fixed, f, f.replace('.txt','.vl.txt'))
        print( cmd )
        if not args.dry_run:
            os.system(cmd)
            #print('Execute {}'.format(cmd))



if __name__ == '__main__':
    main()
