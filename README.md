# Diablo II: Resurrected Single Player Backup

A script to backup all your Diablo II: Resurrected single player characters.

## Motivation

I was working on my single player holy grail when the power went out and one of my character files became corrupted. This also corrupted the shared stash that is used by all single player characters.

After being unable to restore the character, I wrote this script to help prevent this problem in the future.

I was able to rebuilt my character using another tool but I really didn't like how long that took.

## What it does

It will copy all the files in the `C:\Users\<username>\Saved Games\Diablo II Resurrected` folder into the `C:\Users\<username>\Saved Games\Backup\<current_time>` folder.

** You can override these settings in a `config.json` file. ** You can read about this in the [Configuration section](## Configuration)

When you navigate to the `Backups\Diablo II Resurrected` folder, you will see a folder with a timestamp as the name. It will have all your characters in it.

![Backup Sample](images/backup-sample.png)

## How to install and run

- Install Python 3

Use the following command to run this script:

`python backup.py`

The script uses Python. It was tested on Python 3.10+ and uses only standard libraries so it should work with most versions of Python 3.

## Configuration

If you want to change the default `source`, `destination` or `timestamp_format` you can create a `config.json` file. The `config.json.example` file has been provided to make this easier and provide a sample.

### Configuration Settings

- `source`: Where your single player character files are located
- `destination`: Where you want to save a backup at. ** The `timestamp_format` will be added to the end of this path. **
- `timestamp_format`: The Python strftime format codes. You can read about them [here](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes).