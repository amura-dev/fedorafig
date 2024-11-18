import os
import json

from bash import exec_cmd, exec_script


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

  def run_scripts(self):
    with open(self.cfg_main, 'r') as fh:
      data = json.load(fh)
      for entry in data.values():
        if not ('script' in entry and entry['script'] != ''):
          continue
        path = os.path.join(self.cfg_path, 'install-scripts', entry['script'])
        exec_script(path)

  
  def mv_cfgs(self):
    with open(self.cfg_main, 'r') as fh:
      data = json.load(fh)
      for entry in data.values():
        if not ('cfgpath' in entry and entry['cfgpath'] != ''):
          continue
        cfgpath = os.path.join(self.cfg_path, 'configs', entry['cfgpath'])
        syspath = os.path.expanduser(entry['syspath'])
        exec_cmd(f'mkdir -p {syspath}')
        exec_cmd(f'cp -rf {cfgpath}/. {syspath} || \
                   cp -rf {cfgpath} {syspath}')
