import os
from pathlib import Path
from dotenv import load_dotenv

def load_app_env():
    root_directory = Path(__file__).parent.parent.parent.parent.parent

    env_filepath = os.path.join(root_directory, 'iac', '.env')

    load_dotenv(env_filepath)

    os.environ['STAGE'] = 'DEV'