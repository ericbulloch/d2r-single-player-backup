from datetime import datetime
import json
import os
from pathlib import Path
import shutil


def get_variables():
    username = os.environ['USERPROFILE'].split('\\')[-1]
    default_base = os.path.join('C:\\', 'Users', username, 'Saved Games')
    script_path = os.path.abspath(__file__)
    script_directory = os.path.dirname(script_path)
    config_file_path = os.path.join(script_directory, 'config.json')
    config = dict()

    if os.path.isfile(config_file_path):
        print('config.json file was found. Trying to load the file.')
        with open(config_file_path, 'r') as fp:
            config = json.load(fp)
        print('config.json was successfully loaded.')

    if 'source' in config:
        source = config.get('source')
        print(f'Using source path found in config.json ({source})')
    else:
        source = os.path.join(default_base, 'Diablo II Resurrected')
        print(f'Using the default source path ({source})')

    if 'destination' in config:
        destination = config.get('destination')
        print(f'Using destination path found in config.json ({destination})')
    else:
        destination = os.path.join(default_base, 'Backups', 'Diablo II Resurrected')
        print(f'Using the default destination path ({destination})')

    if 'timestamp_format' in config:
        timestamp_format = config.get('timestamp_format')
        print(f'Using timestamp_format found in config.json ({timestamp_format})')
    else:
        timestamp_format = "%Y.%m.%d.%H.%M.%S"
        print(f'Using the default timestamp_format ({timestamp_format})')

    if 'prune' in config:
        prune = config.get('prune')
        print(f'Using prune found in config.json ({prune})')
    else:
        prune = True
        print(f'Using the default prune ({prune})')

    if 'limit_backups' in config:
        limit_backups = config.get('limit_backups')
        print(f'Using limit_backups found in config.json ({limit_backups})')
    else:
        limit_backups = True
        print(f'Using the default limit_backups ({limit_backups})')

    if limit_backups:
        if 'number_of_backups' in config:
            number_of_backups = config.get('number_of_backups')
            print(f'Using number_of_backups found in config.json ({number_of_backups})')
        else:
            number_of_backups = 30
            print(f'Using the default number_of_backups ({number_of_backups})')
    else:
        number_of_backups = -1

    return source, destination, timestamp_format, prune, limit_backups, number_of_backups


def get_most_recent_backup(destination):
    try:
        most_recent = max([d for d in os.listdir(destination) if os.path.isdir(os.path.join(destination, d))])
        if most_recent:
            return most_recent
    except (FileNotFoundError, ValueError):
        return None


def prune_files(base_directory):
    system_files = set(['Settings', 'SharedStashSoftCoreV2'])
    for directory, directories, file_names in os.walk(base_directory):
        if not file_names:
            continue
        keepers = set([name.split('.')[0] for name in file_names if name.endswith('.map')])
        keepers.update(system_files)
        deleted_files = []
        for file_name in file_names:
            name = file_name.split('.')[0]
            if name not in keepers:
                full_path = os.path.join(directory, file_name)
                deleted_files.append(full_path)
                os.remove(full_path)
        if deleted_files:
            print(f'Pruned {directory}')
            for f in deleted_files:
                print(f' - Deleted {f}')


def remove_old_backups(base_destination, number_of_backups):
    backup_folder = Path(base_destination)
    backups = sorted((p for p in backup_folder.iterdir() if p.is_dir()), key=lambda p: p.stat().st_ctime)
    if len(backups) > number_of_backups:
        print(f'\nThere are {len(backups)} backups and there can only be {number_of_backups}')
        print(f'Removing the following {len(backups) - number_of_backups} backups:')
        for b in backups[:-1 * number_of_backups]:
            print(b)
            shutil.rmtree(b)


def main():
    source, base_destination, timestamp_format, prune, limit_backups, number_of_backups = get_variables()
    if prune:
        print('Started pruning files')
        prune_files(base_destination)
        print('Finished pruning files')
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
    if limit_backups:
        remove_old_backups(base_destination, number_of_backups)
    else:
        print('Not limiting the number of backups')
    print('Backup complete!')


if __name__ == '__main__':
    main()
