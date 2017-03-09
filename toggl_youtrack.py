#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from datetime import date, timedelta, datetime
from toggl import TogglDataManager
from youtrack import YoutrackDataManager
import click


@click.command()
@click.option('--track', is_flag=True, default=False, help='tracks time to youtrack from toggl')
@click.option('--format', is_flag=True, default=False, help='formats toggl entries by youtrack tags')
@click.argument('start', default='today')
@click.argument('end', default='tomorrow')
def get_magic_done(track, format, start, end):
    start_date = _process_arg(start)
    end_date = _process_arg(end)

    click.echo(
        'Time interval is from {0:s} to {1:s}'.format(start_date.strftime('%d-%m-%Y'), end_date.strftime('%d-%m-%Y')))

    # initialization
    toggl_data_manager = TogglDataManager()
    youtrack_data_manager = YoutrackDataManager()
    # get time entries from toggl
    toggle_time_entries = toggl_data_manager.load_time_entries(start_date, end_date)

    if len(toggle_time_entries) == 0:
        print('For requested time interval we did not find any entries')
        return

    click.echo('For requested time interval in toggl we found {0:d} entry(-ies):'.format(len(toggle_time_entries)))
    for entry in toggle_time_entries:
        click.echo('name: {0:s}, start time: {1:s}, duration: {2:d} min'.format(
            entry['full_description'],
            entry['start_time'].strftime('%c'),
            entry['duration'] // 60))
    if track:
        click.echo('These time entries will be tracked into youtrack')
        # add time from entries to youtrack
        youtrack_data_manager.track_time(toggle_time_entries)

    if format:
        click.echo('Formatting time entries')
        click.echo('Loading data from youtrack')
        # get tasks, subsystems, tags, etc. from youtrack
        youtrack_tasks = youtrack_data_manager.load_tasks_with_attributes(toggle_time_entries)
        click.echo('Putting data to toggl')
        # add data from youtrack (description, tags, subsystems) to toggl time entries
        toggl_data_manager.format_time_entries(toggle_time_entries, youtrack_tasks)
        click.echo('Done')


def _process_arg(dt):
    if dt == 'today':
        return date.today()
    elif dt == 'yesterday':
        return date.today() - timedelta(days=1)
    elif dt == 'tomorrow':
        return date.today() + timedelta(days=1)
    else:
        dt_parsed = datetime.strptime(dt, '%d-%m-%Y')
        return dt_parsed.date()


if __name__ == '__main__':
    get_magic_done()
