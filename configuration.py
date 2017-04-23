import json
from pathlib import Path
import os


def load_config(default_path='config.json', env_key='CFG'):
    path = Path(default_path)
    value = os.getenv(env_key, None)
    if value:
        path = Path(value)
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    else:
        raise FileNotFoundError('No config found by path "{}"'.format(path))

config = load_config()

class TogglConfig:
    YOUTRACK_TASKS_ID_CONST = config['youtrack']['tasks_prefix']
    WORKSPACE_NAME = config['toggl']['workspace']
    LOGIN = config['toggl']['login']
    PASS = config['toggl']['password']
    AUTH_URL = 'https://www.toggl.com/api/v8/me'
    GET_ENTRIES_URL = 'https://www.toggl.com/api/v8/time_entries'
    GET_WORKSPACES_URL = 'https://www.toggl.com/api/v8/workspaces'
    TOKEN_PASS = 'api_token'


class YoutrackConfig:
    YOUTRACK_URL = config['youtrack']['link']
    LOGIN = config['youtrack']['login']
    PASS = config['youtrack']['password']
    ISSUE_ID_CONST = '{issue_id}'
    LOGIN_URL = YOUTRACK_URL + '/rest/user/login'
    WORKITEM_URL = YOUTRACK_URL + '/rest/issue/' + ISSUE_ID_CONST + '/timetracking/workitem'
    ISSUE_URL = YOUTRACK_URL + '/rest/issue/' + ISSUE_ID_CONST
