#!/usr/bin/env python3
#TODO: Make sure `sudo` password is entered on run and never asked again.
#TODO: Utility to be stored in `.local`.
#TODO: Change output messages.
#TODO: Add a way to easily access custom commonly-run scripts.
#TODO: Activate only required repositories to increase check speed.
#TODO: Add a way to set up runtime scripts.

import os
import argparse
import subprocess

import cfg
from check import Checker
from run import Runner

CHECKER = Checker(cfg.FEDORAFIG_CFG_PATH, cfg.FEDORAFIG_SRC_PATH)
RUNNER = Runner(cfg.FEDORAFIG_CFG_PATH, cfg.FEDORAFIG_SRC_PATH)


def main():
    parser = argparse.ArgumentParser(
        description="Configure Fedora with a single utility",
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(title="Commands", dest='command')
    
    run_help = """RUN"""
    run_parser = subparsers.add_parser('run', help=run_help)
    run_parser.set_defaults(func=run)

    check_help = """
    Checks syntax of and paths specified in all configuration files, checks all repositories for validity and all packages specified.
    """
    check_parser = subparsers.add_parser('check', help=check_help)
    check_parser.set_defaults(func=check)

    args = parser.parse_args()
    if 'func' in args:
        args.func(args)
    else:
        parser.print_help()
        exit(1)


def check(args):
  print("Checking paths and syntax in `main.json`...")
  CHECKER.main_cfg_check()
  print("Done.")

  print("Checking existence of packages specified in `main.json`...")
  CHECKER.pkgs_check()
  print("Done.")
  
  print("Saving `SHA256SUM`...")
  print(f"DEBUG: SHA256SUM: {CHECKER.get_checksum()}")
  checksum_file = os.path.join(CHECKER.src_path, 'SHA256SUM')
  with open(checksum_file, 'w+') as fh:
    fh.write(CHECKER.get_checksum())
  print("Done.")


def run(args):
  print("Checking checksums...")
  checksum_file = os.path.join(CHECKER.src_path, 'SHA256SUM')
  if not (os.path.exists(checksum_file) and os.path.isfile(checksum_file)):
    check([])

  cur_checksum = CHECKER.get_checksum()
  old_checksum = ''
  with open(checksum_file, 'r') as fh:
    old_checksum = fh.readline()
  if cur_checksum != old_checksum:
    check([])
  print(f"DEBUG: {cur_checksum}")
  print("Done.")

  print("Installing packages...")
  RUNNER.install_pkgs()
  print("Done.")


if __name__ == '__main__':
  main()
