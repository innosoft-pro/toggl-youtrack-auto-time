class TogglConfig:
    TOKEN = 'EnterYourToken'
    GET_ENTRIES_URL = 'https://www.toggl.com/api/v8/time_entries'
    TOKEN_PASS = 'api_token'
    YOUTRACK_TASKS_ID = 'MMX'


class YoutrackConfig:
    LOGIN_URL = 'http://youtrack.innosoft.pro:8080/rest/user/login'
    WORKITEM_URL = 'http://youtrack.innosoft.pro:8080/rest/issue/{issue_id}/timetracking/workitem'
    ISSUE_ID_CONST = '{issue_id}'

    LOGIN = 'EnterYourLogin'
    PASS = 'EnterYourPassword'
