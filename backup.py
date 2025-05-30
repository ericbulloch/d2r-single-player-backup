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

    return source, destination, timestamp_format, prune


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


def main():
    source, base_destination, timestamp_format, prune = get_variables()
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
    print('Backup complete!')


if __name__ == '__main__':
    main()
