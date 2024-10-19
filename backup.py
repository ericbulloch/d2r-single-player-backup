from datetime import datetime
import os
import shutil


def main(time, destination, username):
    print(f'Saving backup with timestamp {time}')
    source = rf"C:\Users\{username}\Saved Games\Diablo II Resurrected"
    print(f"Saving the '{source}' directory to the '{destination}' directory")
    shutil.copytree(source, destination)


if __name__ == '__main__':
    time = datetime.now().strftime("%Y.%m.%d.%H.%M.%S")
    username = os.environ['USERPROFILE'].split('\\')[-1]
    base = f'C:\\Users\\{username}\\Saved Games\\Backups'
    try:
        most_recent = max([d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))])
        if most_recent:
            print(f'Most recent update was on {most_recent}')
    except (FileNotFoundError, ValueError):
        pass
    destination = f"{base}\\{time}\\Diablo II Resurrected"
    main(time, destination, username)