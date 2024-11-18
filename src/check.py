import os
import json
import hashlib
import subprocess

from errors import PathError, SyntaxError



class Checker():
  def __init__(self, cfg_path, bin_path):
    self.cfg_path = cfg_path
    self.bin_path = bin_path
    self.cfg_main = os.path.join(cfg_path, 'main.json')


  def cfg_main_check(self):
    if not (os.path.exists(self.cfg_main) and os.path.isfile(self.cfg_main)):
      raise PathError(f"File not found {self.cfg_main}")

    with open(self.cfg_main, 'r') as fh:
      print("DEBUG: Loading `main.json`...")
      data = json.load(fh)
      if not isinstance(data, dict):
        raise SyntaxError(f"In `main.json`: Outermost object must be `dict`")

      for entry in data.values():
        print("DEBUG: Checking datatypes...")
        if not isinstance(entry, dict):
          raise SyntaxError(f"In `main.json`: Outermost value must be `dict`")

        print("DEBUG: Checking `cfgpath` syntax...")
        if 'cfgpath' in entry and entry['cfgpath'] != '':
          if 'syspath' not in entry or entry['syspath'] == '':
            raise SyntaxError(f"In `main.json`: `syspath` must accompany the `cfgpath`: {entry['cfgpath']}")

          path = f'{self.cfg_path}/configs/{entry['cfgpath']}'
          if not os.path.exists(path):
            raise PathError(f"In `main.json`: `cfgpath` not found: {entry['cfgpath']}")

        print("DEBUG: Checking `repo` syntax...")
        if 'repo' in entry and entry['repo'] != '':
          if 'package' not in entry or entry['package'] == '':
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
    with open(self.cfg_main, 'r') as fh:
      data = json.load(fh)
      for entry in data.values():
        if 'package' in entry:
          pkgs.append(entry['package'])
    
    with open('/tmp/fedorafig-packages.txt', 'w+') as fh:
      for pkg in pkgs:
        print(f"DEBUG: Package: `{pkg}`.")
        fh.write(f'{pkg}\n')

    self.exec_script('pkgs_check.sh')


  def exec_script(self, script_name):
    path = f'{self.bin_path}/{script_name}'
    env = os.environ.copy()
    env['FEDORAFIG_CFG_PATH'] = self.cfg_path
    env['FEDORAFIG_BIN_PATH'] = self.bin_path

    subprocess.run(['chmod', 'u+x', path], check=False)
    subprocess.run(['bash', path], env=env, check=False)


  def get_checksum(self):
    hasher = hashlib.sha256()
    for root, _, files in os.walk(self.cfg_path):
      for file in sorted(files):
        path = os.path.join(root, file)
        with open(path, 'rb') as fh:
          while chunk := fh.read(8192):
            hasher.update(chunk)

    return hasher.hexdigest()
