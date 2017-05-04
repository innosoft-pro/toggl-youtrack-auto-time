from configuration import TogglConfig, YoutrackConfig
import requests
import json
from dateutil.parser import parse


class TogglDataManager:
    def __init__(self):
        self.token = self._authenticate()

    def is_current_time_entry_exist(self):
        result = requests.get(TogglConfig.GET_CURRENT_ENTRY_URL, auth=(TogglConfig.LOGIN, TogglConfig.PASS))
        result.raise_for_status()
        entry = json.loads(result.text)
        if entry['data'] is None:
            return False
        else:
            return True

    def _authenticate(self):
        result = requests.get(TogglConfig.AUTH_URL, auth=(TogglConfig.LOGIN, TogglConfig.PASS))
        result.raise_for_status()
        info = json.loads(result.text)
        return info['data']['api_token']

    def load_time_entries(self, start_datetime=None, end_datetime=None):
        """
        method loads all time entries from start time to end time. If time is not specified,
        loads data for 9 last days or 1000 entries (constraint on API level).
        :param start_datetime: datetime
        :param end_datetime: datetime
        :return: list of time entries. Each entry contains toggl_id, youtrack_id, full_description,
        duration (sec), start_date (datetime with timezone).
        """
        if start_datetime is not None:
            st_dt_str = start_datetime.isoformat()
        else:
            st_dt_str = None

        if end_datetime is not None:
            end_dt_str = end_datetime.isoformat()
        else:
            end_dt_str = None

        params = {
            'start_date': st_dt_str,
            'end_date': end_dt_str
        }

        result = requests.get(TogglConfig.GET_ENTRIES_URL, auth=(self.token, TogglConfig.TOKEN_PASS), params=params)

        result.raise_for_status()

        preprocessed_entries = self._preprocess_entries(result.text)

        return preprocessed_entries

    def _preprocess_entries(self, result_text):
        entries_list = json.loads(result_text)
        result = []
        for entry in entries_list:
            if entry['duration'] > 30 and entry['description'].startswith(TogglConfig.YOUTRACK_TASKS_ID_CONST):
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
        workspace_id = self._load_workspace_id()
        projects_ids = self._load_project_ids(workspace_id)

        for time_entry in toggle_time_entries:
            url = TogglConfig.GET_ENTRIES_URL + '/' + str(time_entry['toggl_id'])

            if 'Subsystem' in youtrack_tasks[time_entry['youtrack_id']]:
                tags = [youtrack_tasks[time_entry['youtrack_id']]['Subsystem']]
            else:
                tags = []

            if self._is_me_reviewer(youtrack_tasks[time_entry['youtrack_id']]):
                project_id = projects_ids['Quality management']
            elif youtrack_tasks[time_entry['youtrack_id']]['tag']:
                project_id = projects_ids[youtrack_tasks[time_entry['youtrack_id']]['tag'][0]]
            else:
                project_id = None

            new_time_entry = self._get_time_entry_template(
                time_entry['youtrack_id'] + ' ' + youtrack_tasks[time_entry['youtrack_id']]['summary'],
                time_entry['toggl_id'],
                project_id,
                workspace_id,
                tags
            )
            result = requests.put(url, auth=(self.token, TogglConfig.TOKEN_PASS),
                                  data=json.dumps(new_time_entry))
            result.raise_for_status()

    def _is_me_reviewer(self, yt_record):
        if YoutrackConfig.REVIEWER in yt_record:
            reviewer = yt_record[YoutrackConfig.REVIEWER]
            if (type(reviewer) is str and
                        reviewer == YoutrackConfig.LOGIN) or \
                    (type(reviewer) is list and
                             len(reviewer) >= 2 and
                             YoutrackConfig.LOGIN in reviewer):
                return True

    def _load_workspace_id(self):
        result = requests.get(TogglConfig.GET_WORKSPACES_URL, auth=(self.token, TogglConfig.TOKEN_PASS))
        workspaces_list = result.json()
        workspace_id = 0
        for workspace in workspaces_list:
            if workspace['name'] == TogglConfig.WORKSPACE_NAME:
                workspace_id = workspace['id']

        if workspace_id == 0:
            raise RuntimeError('No workspace found')
        return workspace_id

    def _load_project_ids(self, workspace_id):
        projects_url = TogglConfig.GET_WORKSPACES_URL + '/' + str(workspace_id) + '/projects'
        result = requests.get(projects_url, auth=(self.token, TogglConfig.TOKEN_PASS))
        projects_list = result.json()
        result_dict = {}
        for project in projects_list:
            result_dict[project['name']] = project['id']
        return result_dict

    def _get_time_entry_template(self, description, id, pid, wid, tags):
        return {
            "time_entry": {
                "description": description,
                "id": id,
                "pid": pid,
                "wid": wid,
                "tags": tags
            }
        }
