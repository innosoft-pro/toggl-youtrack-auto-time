class TogglConfig:
    TOKEN = 'EnterYourToken'
    GET_ENTRIES_URL = 'https://www.toggl.com/api/v8/time_entries'
    TOKEN_PASS = 'api_token'
    YOUTRACK_TASKS_ID_CONST = 'MMX'


class YoutrackConfig:
    YOUTRACK_URL = 'EnterYourYoutrackURL'
    LOGIN_URL = YOUTRACK_URL+'/rest/user/login'
    WORKITEM_URL = YOUTRACK_URL+'/rest/issue/{issue_id}/timetracking/workitem'
    ISSUE_ID_CONST = '{issue_id}'

    LOGIN = 'EnterYourLogin'
    PASS = 'EnterYourPassword'
