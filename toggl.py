from config import TogglConfig
import requests
import json
from pytz import utc
from datetime import datetime
from dateutil.parser import parse


class TogglDataManager:
    def __init__(self):
        pass

    def load_time_entries(self, start_date=None, end_date=None):
        """
        method loads all time entries from start time to end time. If time is not specified,
        loads data for 9 last days or 1000 entries (constraint on API level).
        :param start_date: datetime
        :param end_date: datetime
        :return: list of time entries. Each entry contains toggl_id, youtrack_id, full_description,
        duration (sec), start_date (datetime with timezone).
        """
        if start_date is not None:
            st_dt_str = datetime(year=start_date.year, month=start_date.month, day=start_date.day, hour=0, minute=0,
                                 second=0, tzinfo=utc).isoformat()
        else:
            st_dt_str = None

        if end_date is not None:
            end_dt_str = datetime(year=end_date.year, month=end_date.month, day=end_date.day, hour=0, minute=0,
                                  second=0, tzinfo=utc).isoformat()
        else:
            end_dt_str = None

        params = {
            'start_date': st_dt_str,
            'end_date': end_dt_str
        }

        result = requests.get(TogglConfig.GET_ENTRIES_URL, auth=(TogglConfig.TOKEN, TogglConfig.TOKEN_PASS),
                              params=params)

        result.raise_for_status()

        preprocessed_entries = self._preprocess_entries(result.text)

        return preprocessed_entries

    def _preprocess_entries(self, result_text):
        entries_list = json.loads(result_text)
        result = []
        for entry in entries_list:
            if entry['duration'] > 0 and entry['description'].startswith(TogglConfig.YOUTRACK_TASKS_ID_CONST):
                result.append({
                    'toggl_id': entry['id'],
                    'youtrack_id': entry['description'].strip().split(' ')[0],
                    'full_description': entry['description'],
                    'duration': entry['duration'],
                    'start_time': parse(entry['start'])
                })
        return result

    def format_time_entries(self, toggle_time_entries, youtrack_tasks):
        """
        maps entries to youtrack tasks: set projects, tags, etc.
        :param toggle_time_entries: list of time entries. Each entry contains toggl_id, youtrack_id,
        full_description, duration (sec).
        :param youtrack_tasks: dict. key is youtrack issue id (example - MMX-111), value is object
        that contains following data:
        subsystem: str
        tags: list of str
        name: str
        :return:
        """
        pass
