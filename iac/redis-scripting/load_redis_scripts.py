import os
from pathlib import Path

def load_redis_scripts():
    root_dirpath = Path(__file__).parent
    scripts_dirpath = os.path.join(root_dirpath, 'scripts')

    for filename in os.listdir(scripts_dirpath):
        script_filepath = os.path.join(scripts_dirpath, filename)

        with open(script_filepath, 'r') as file:
            flattened_content = file.read() \
                .replace('\n', '')

            cmd = f'SCRIPT LOAD \'{flattened_content}\''
            print(cmd)

if __name__ == '__main__':
    load_redis_scripts()