import base64
import uuid
import os
from config import WEB_UPLOADDIR
from jwt import decode
from app import app
from core.models import ServerMode

def run_cmd(cmd):
  return os.popen(cmd).read()

def run_argv(argv):
  import subprocess
  try:
    return subprocess.run(argv, capture_output=True, text=True, timeout=60).stdout
  except Exception as e:
    return str(e)

def initialize():
  return run_cmd('python3 setup.py')

def generate_uuid():
  return str(uuid.uuid4())[0:6]

def decode_base64(text):
  return base64.b64decode(text).decode('utf-8')

def get_identity(token):
  return decode(token, app.config["JWT_SECRET_KEY"], algorithms=["HS256"], options={"verify_exp":False}).get('identity')

def save_file(filename, text):
  try:
    filename = os.path.basename(filename)
    filepath = os.path.join(WEB_UPLOADDIR, filename)
    if os.path.dirname(os.path.abspath(filepath)) != os.path.abspath(WEB_UPLOADDIR):
      return 'Filename is not allowed'
    f = open(filepath, 'w')
    f.write(text)
    f.close()
  except Exception as e:
    print('File upload failed: {}'.format(e))
    text = 'File upload failed.'
  return text

def is_level_easy():
  mode = ServerMode.query.one()
  return mode.hardened == False

def is_level_hard():
  mode = ServerMode.query.one()
  return mode.hardened == True

def set_mode(mode):
  mode = ServerMode.set_mode(mode)
