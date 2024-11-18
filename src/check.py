import os
import json
import hashlib

from bash import exec_script, exec_cmd
from errors import PathError, SyntaxError



class Checker():
  def __init__(self, cfg_path, src_path):
    self.cfg_path = cfg_path
    self.src_path = src_path
    self.main_cfg = os.path.join(cfg_path, 'main.json')


  def main_cfg_check(self):
    if not (os.path.exists(self.main_cfg) and os.path.isfile(self.main_cfg)):
      raise PathError(f"File not found {self.main_cfg}")

    with open(self.main_cfg, 'r') as fh:
      print("DEBUG: Loading `main.json`...")
      data = json.load(fh)
      if not isinstance(data, dict):
        raise SyntaxError(f"In `main.json`: Outermost object must be `dict`")

      for entry in data.values():
        print("DEBUG: Checking datatypes...")
        if not isinstance(entry, dict):
          raise SyntaxError(f"In `main.json`: Outermost value must be `dict`")

        print("DEBUG: Checking `cfgpath` syntax...")
        if 'cfgpath' in entry:
          if 'syspath' not in entry:
            raise SyntaxError(f"In `main.json`: `syspath` must accompany the `cfgpath`: {entry['cfgpath']}")
            
          if entry['cfgpath'] != '' and entry['syspath'] != '':
            cfgpath = os.path.join(self.cfg_path, 'configs', entry['cfgpath'])
            if not os.path.exists(cfgpath):
              raise PathError(f"`cfgpath` not found: {cfgpath}")
            # No need to check syspath because it will be created anyway

          elif entry['cfgpath'] == '' and entry['syspath'] == '':
            pass
          else:
            raise SyntaxError(f"`cfgpath` and `syspath` must either both be blank or specified: {cfgpath}")

          path = f'{self.cfg_path}/configs/{entry['cfgpath']}'
          if not os.path.exists(path):
            raise PathError(f"In `main.json`: `cfgpath` not found: {entry['cfgpath']}")

        print("DEBUG: Checking `repo` syntax...")
        if 'repo' in entry:
          if 'package' not in entry:
            raise SyntaxError(f"In `main.json`: `repo` must be accompanied by `package`")
          if not self.repo_exists(entry['repo']):
            raise SyntaxError(f"In `main.json`: `repo` not found: {entry['repo']}")

        print("DEBUG: Checking `script` syntax...")
        if 'script' in entry and entry['script'] != '':
          path = f'{self.cfg_path}/install-scripts/{entry['script']}'
          if not os.path.exists(path) and os.path.isfile(path):
            raise PathError(f"In `main.json`: `script` not found: {entry['script']}")


  def repo_exists(self, repo_str):
    repos_dir = os.path.join(self.cfg_path, 'repos')
    print(f"DEBUG: repos_dir: `{repos_dir}`")
    for file in os.listdir(repos_dir):
      print(f"DEBUG: file: `{file}`")
      path = os.path.join(repos_dir, file)
      with open(path, 'r') as fh:
        for line in fh:
          if line.strip() == f'[{repo_str}]':
            return True
    
    return False


  def pkgs_check(self):
    print("DEBUG: Checking existence of packages...")
    pkgs = []
    with open(self.main_cfg, 'r') as fh:
      data = json.load(fh)
      for entry in data.values():
        if 'package' in entry:
          pkgs.append(entry['package'])

    with open('/tmp/fedorafig-packages.txt', 'w+') as fh:
      for pkg in pkgs:
        print(f"DEBUG: Package: `{pkg}`.")
        fh.write(f'{pkg}\n')

    exec_script('pkgs_check.sh')

    '''
    repos_dir = '/etc/yum.repos.d/'
    for file in os.listdir(repos_dir):
      path = os.path.join(repos_dir, file)
      with open(path, 'r') as fh:
        for line in fh:
          baseurl = ''
          if line.find('baseurl=') != -1:
            baseurl = line[line.find('=')+1:].strip()
            print(f"DEBUG: Base url: {baseurl}")
          if baseurl != '':
            exec_cmd(f'sudo rpm --import {baseurl}')
    '''

  def get_checksum(self):
    hasher = hashlib.sha256()
    for root, _, files in os.walk(self.cfg_path):
      for file in sorted(files):
        path = os.path.join(root, file)
        with open(path, 'rb') as fh:
          while chunk := fh.read(8192):
            hasher.update(chunk)

    return hasher.hexdigest()
