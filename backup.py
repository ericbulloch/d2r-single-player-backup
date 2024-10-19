from datetime import datetime
import json
import os
import shutil


def get_variables():
    username = os.environ['USERPROFILE'].split('\\')[-1]
    default_base = os.path.join('C:\\', 'Users', username, 'Saved Games')
    config_file_path = 'config.json'
    config = dict()

    if os.path.isfile(config_file_path):
        print('config.json file was found. Trying to load the file.')
        with open(config_file_path, 'r') as fp:
            config = json.load(fp)
        print('config.json was successfully loaded.')

    if config.get('source'):
        source = config.get('source')
        print(f'Using source path found in config.json ({source})')
    else:
        source = os.path.join(default_base, 'Diablo II Resurrected')
        print(f'Using the default source path ({source})')

    if config.get('destination'):
        destination = config.get('destination')
        print(f'Using destination path found in config.json ({destination})')
    else:
        destination = os.path.join(default_base, 'Backups')
        print(f'Using the default destination path ({destination})')

    return source, destination


def get_most_recent_backup(destination):
    try:
        most_recent = max([d for d in os.listdir(destination) if os.path.isdir(os.path.join(destination, d))])
        if most_recent:
            return most_recent
            # print(f'Most recent update was on {most_recent}')
    except (FileNotFoundError, ValueError):
        return None


def main():
    source, base_destination = get_variables()
    most_recent = get_most_recent_backup(base_destination)
    if most_recent:
        print('')
        print(f'Most recent backup was on {most_recent}')
    time = datetime.now().strftime("%Y.%m.%d.%H.%M.%S")
    print('')
    print(f'Using timestamp {time} for this backup folder name')
    print('')
    destination = os.path.join(base_destination, time, "Diablo II Resurrected")
    print(f"Saving the '{source}' directory to the '{destination}' directory")
    shutil.copytree(source, destination)
    print('Backup complete!')


if __name__ == '__main__':
    main()