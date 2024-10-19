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
        destination = os.path.join(default_base, 'Backups', 'Diablo II Resurrected')
        print(f'Using the default destination path ({destination})')

    if config.get('timestamp_format'):
        timestamp_format = config.get('timestamp_format')
        print(f'Using timestamp_format found in config.json ({timestamp_format})')
    else:
        timestamp_format = "%Y.%m.%d.%H.%M.%S"
        print(f'Using the default timestamp_format ({timestamp_format})')

    return source, destination, timestamp_format


def get_most_recent_backup(destination):
    try:
        most_recent = max([d for d in os.listdir(destination) if os.path.isdir(os.path.join(destination, d))])
        if most_recent:
            return most_recent
            # print(f'Most recent update was on {most_recent}')
    except (FileNotFoundError, ValueError):
        return None


def main():
    source, base_destination, timestamp_format = get_variables()
    most_recent = get_most_recent_backup(base_destination)
    if most_recent:
        print('')
        print(f'Most recent backup was on {most_recent}')
    time = datetime.now().strftime(timestamp_format)
    print('')
    print(f'Using timestamp {time} for this backup folder name')
    print('')
    destination = os.path.join(base_destination, time)
    print(f"Saving the '{source}' directory to the '{destination}' directory")
    shutil.copytree(source, destination)
    print('Backup complete!')


if __name__ == '__main__':
    main()