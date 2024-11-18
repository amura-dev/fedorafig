#!/usr/bin/env python3

import os
import argparse

from check import Checker

# File path can be any directory. Do not include the end `/`.
FEDORAFIG_CFG_PATH = os.path.expanduser('~/.config/fedorafig')
FEDORAFIG_BIN_PATH = os.path.expanduser('~/bin/fedorafig-src')


def main():
    parser = argparse.ArgumentParser(
        description="Configure Fedora with a single utility",
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(title="Commands", dest='command')
    
    run_help = """RUN"""
    run_parser = subparsers.add_parser('run', help=run_help)
    run_parser.set_defaults(func=run)

    check_help = """CHECK"""
    check_parser = subparsers.add_parser('check', help=check_help)
    check_parser.set_defaults(func=check)

    args = parser.parse_args()
    if 'func' in args:
        args.func(args)
    else:
        parser.print_help()
        exit(1)


def check(args):
  checker = Checker(FEDORAFIG_CFG_PATH, FEDORAFIG_BIN_PATH)

  print("Checking paths and syntax in `main.json`...")
  checker.cfg_main_check()
  print("Done.")

  print("Checking existence of packages specified in `main.json`...")
  checker.pkgs_check()
  print("Done.")
  
  print("Saving `SHA256SUM`...")
  print(f"DEBUG: SHA256SUM: {checker.get_checksum()}")
  checksum_file = os.path.join(checker.bin_path, 'SHA256SUM')
  with open(checksum_file, 'w+') as fh:
    fh.write(checker.get_checksum())
  print("Done.")


def run(args):
  pass


if __name__ == '__main__':
  main()
