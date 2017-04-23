#!/usr/bin/env python3

from datetime import date, timedelta, datetime
from toggl import TogglDataManager
from youtrack import YoutrackDataManager
from configuration import load_last_datetime, set_last_datetime
import pytz
import click


@click.command()
@click.option('--track', is_flag=True, default=False, help='tracks time to youtrack from toggl')
@click.option('--format', is_flag=True, default=False, help='formats toggl entries by youtrack tags')
@click.option('--since_last', is_flag=True, default=False, help='track all data since last launch')
@click.option('--starting_from', default='today', help='date when start track time')
@click.option('--until', default='tomorrow', help='date when stop track time')
def get_magic_done(track, format, since_last, starting_from, until):
    if since_last:
        try:
            last_time = load_last_datetime()
        except (FileNotFoundError, ValueError) as e:
            click.echo(e)
            return
        start_datetime = last_time
        end_datetime = datetime.utcnow().replace(tzinfo=pytz.utc)
    else:
        start_datetime = _process_arg(starting_from)
        end_datetime = _process_arg(until)

    set_last_datetime(end_datetime)

    # initialization
    toggl_data_manager = TogglDataManager()
    youtrack_data_manager = YoutrackDataManager()

    # check current time entry
    if toggl_data_manager.is_current_time_entry_exist():
        click.echo('Please stop running time entry, otherwise tracking problems might occur. Application stopped.')
        return

    click.echo(
        'Time interval is from {0:s} until {1:s}'.format(start_datetime.strftime('%d-%m-%Y %H:%M:%S'),
                                                         end_datetime.strftime('%d-%m-%Y %H:%M:%S')))

    # get time entries from toggl
    toggle_time_entries = toggl_data_manager.load_time_entries(start_datetime, end_datetime)

    if len(toggle_time_entries) == 0:
        print('For requested time interval we did not find any entries. Application stopped.')
        return

    click.echo('For requested time interval in toggl we found {0:d} entry(-ies):'.format(len(toggle_time_entries)))
    for entry in toggle_time_entries:
        click.echo('name: {0:s}, start time: {1:s}, duration: {2:d} min'.format(
            entry['full_description'],
            entry['start_time'].strftime('%c'),
            round(entry['duration'] / 60)))
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
        return _convert_date_to_datetime(date.today())
    elif dt == 'yesterday':
        return _convert_date_to_datetime(date.today() - timedelta(days=1))
    elif dt == 'tomorrow':
        return _convert_date_to_datetime(date.today() + timedelta(days=1))
    else:
        try:
            return datetime.strptime(dt, '%d-%m-%Y').replace(tzinfo=pytz.utc)
        except ValueError:
            return datetime.strptime(dt, '%d-%m-%Y %H:%M:%S').replace(tzinfo=pytz.utc)


def _convert_date_to_datetime(dt):
    return datetime(year=dt.year, month=dt.month, day=dt.day, hour=0, minute=0,
                    second=0, tzinfo=pytz.utc)


if __name__ == '__main__':
    get_magic_done()
