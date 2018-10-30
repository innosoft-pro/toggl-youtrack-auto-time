import json
from datetime import datetime
from pathlib import Path
import os
import pytz


ENV_CONFIG_KEY = 'CFG'
CONFIGS_FOLDER_PATH = Path('configs')
DATA_PATH = CONFIGS_FOLDER_PATH.joinpath('launch_data.json')
DT_FORMAT = '%d-%m-%Y %H:%M:%S %Z'


def get_config_path():
    default_path = CONFIGS_FOLDER_PATH.joinpath('config.json')
    nondefault_path = os.getenv(ENV_CONFIG_KEY, None)
    if nondefault_path:
        return CONFIGS_FOLDER_PATH.joinpath(nondefault_path)
    else:
        return default_path


def load_config():
    path = get_config_path()
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    else:
        raise FileNotFoundError('No config found by path "{}"'.format(path))


def load_last_datetime():
    config_name = get_config_path().name
    error_msg = 'No previous tracks with config {} found, use other track commands first'.format(config_name)
    if not DATA_PATH.exists():
        raise FileNotFoundError(error_msg)
    data = json.loads(DATA_PATH.read_text(encoding='utf-8'))
    if config_name not in data.keys():
        raise ValueError(error_msg)
    return datetime.strptime(data[config_name], DT_FORMAT).replace(tzinfo=pytz.utc)


def set_last_datetime(dt):
    config_name = get_config_path().name
    if DATA_PATH.exists():
        data = json.loads(DATA_PATH.read_text(encoding='utf-8'))
    else:
        data = {}
    data[config_name] = dt.strftime(DT_FORMAT)
    DATA_PATH.write_text(json.dumps(data, indent=True), encoding='utf-8')


config = load_config()


class TogglConfig:
    YOUTRACK_TASKS_ID_CONST = config['youtrack']['tasks_prefix']
    WORKSPACE_NAME = config['toggl']['workspace']
    LOGIN = config['toggl'].get('login')
    PASS = config['toggl'].get('password')
    TOKEN = config['toggl'].get('token')
    AUTH_URL = 'https://www.toggl.com/api/v8/me'
    GET_ENTRIES_URL = 'https://www.toggl.com/api/v8/time_entries'
    GET_CURRENT_ENTRY_URL = GET_ENTRIES_URL + '/current'
    GET_WORKSPACES_URL = 'https://www.toggl.com/api/v8/workspaces'
    TOKEN_PASS = 'api_token'
    REVIEW = 'review'


class YoutrackConfig:
    YOUTRACK_URL = config['youtrack']['link']
    LOGIN = config['youtrack'].get('login')
    TOKEN = config['youtrack'].get('token')
    PASS = config['youtrack'].get('password')
    ISSUE_ID_CONST = '{issue_id}'
    LOGIN_URL = YOUTRACK_URL + '/rest/user/login'
    TOKEN_URL = YOUTRACK_URL + '/rest/oauth2/token'
    WORKITEM_URL = YOUTRACK_URL + '/rest/issue/' + ISSUE_ID_CONST + '/timetracking/workitem'
    ISSUE_URL = YOUTRACK_URL + '/rest/issue/' + ISSUE_ID_CONST
    # youtrack fields
    SUMMARY = 'summary'
    SUBSYSTEM = 'Subsystem'
    REVIEWER = 'Reviewer'
    STAR = 'Star'
