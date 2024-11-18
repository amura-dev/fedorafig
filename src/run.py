import os
import json

from bash import exec_cmd


class Runner():
  def __init__(self, cfg_path, src_path):
    self.cfg_path = cfg_path
    self.src_path = src_path
    self.cfg_main = os.path.join(cfg_path, 'main.json')
    self.pkgs_n_repos = []

    
  def install_pkgs(self):
    with open(self.cfg_main, 'r') as fh:
      data = json.load(fh)
      for entry in data.values():
        pkg, repo = '', ''
        if 'repo' in entry and entry['repo'] != '':
          repo = entry['repo']
        if 'package' in entry and entry['package'] != '':
          pkg = entry['package']
          pkg_n_repo = (pkg, repo)
          self.pkgs_n_repos.append(pkg_n_repo)
    
    for pkg_n_repo in self.pkgs_n_repos:
      pkg = pkg_n_repo[0]
      repo = pkg_n_repo[1]
      cmd = f'sudo dnf install -y {pkg}'
      if repo != '':
        cmd += f' --enablerepo={repo}'
      exec_cmd(cmd)
