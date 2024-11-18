import os
import subprocess

from cfg import FEDORAFIG_CFG_PATH, FEDORAFIG_SRC_PATH


def exec_script(script_name):
  path = os.path.join(FEDORAFIG_SRC_PATH, script_name)
  env = os.environ.copy()
  env['FEDORAFIG_CFG_PATH'] = FEDORAFIG_CFG_PATH
  env['FEDORAFIG_SRC_PATH'] = FEDORAFIG_SRC_PATH

  subprocess.run(['chmod', 'u+x', path], check=True)
  subprocess.run(['bash', path], env=env, check=True)


def exec_cmd(cmd):
  env = os.environ.copy()
  env['FEDORAFIG_CFG_PATH'] = FEDORAFIG_CFG_PATH
  env['FEDORAFIG_SRC_PATH'] = FEDORAFIG_SRC_PATH
  subprocess.run(['bash', '-c', cmd], check=True)
