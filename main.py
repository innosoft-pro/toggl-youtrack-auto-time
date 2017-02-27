#!/usr/bin/env python3

from datetime import date
from toggl import TogglDataManager
from youtrack import YoutrackDataManager


def get_magic_done():
    # initialization
    toggl_data_manager = TogglDataManager()
    youtrack_data_manager = YoutrackDataManager()

    # get time entries from toggl
    toggle_time_entries = toggl_data_manager.load_time_entries(date.today())

    if len(toggle_time_entries) == 0:
        print('we did not find any entries')
        return

    print('For current day in toggl we found {0:d} entry(-ies):'.format(len(toggle_time_entries)))
    for entry in toggle_time_entries:
        print(entry)

    print('These time entries will be tracked into youtrack')
    # add time from entries to youtrack
    youtrack_data_manager.track_time(toggle_time_entries)

    # get tasks, subsystems, tags, etc. from youtrack
    youtrack_tasks = youtrack_data_manager.load_tasks_with_attributes(toggle_time_entries)

    # add data from youtrack (description, tags, subsystems) to toggl time entries
    toggl_data_manager.format_time_entries(toggle_time_entries, youtrack_tasks)


if __name__ == '__main__':
    get_magic_done()
