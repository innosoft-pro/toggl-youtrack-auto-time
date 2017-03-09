#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


class TogglConfig:
    # can be changed
    YOUTRACK_TASKS_ID_CONST = 'MMX'
    WORKSPACE_NAME = 'Минимакс'
    LOGIN = '<FILL ME PLEASE>'
    PASS = '<FILL ME PLEASE>'
    # constant
    AUTH_URL = 'https://www.toggl.com/api/v8/me'
    GET_ENTRIES_URL = 'https://www.toggl.com/api/v8/time_entries'
    GET_WORKSPACES_URL = 'https://www.toggl.com/api/v8/workspaces'
    TOKEN_PASS = 'api_token'


class YoutrackConfig:
    # can be changed
    YOUTRACK_URL = '<FILL ME PLEASE>'
    LOGIN = '<FILL ME PLEASE>'
    PASS = '<FILL ME PLEASE>'
    # constant
    ISSUE_ID_CONST = '{issue_id}'
    LOGIN_URL = YOUTRACK_URL + '/rest/user/login'
    WORKITEM_URL = YOUTRACK_URL + '/rest/issue/' + ISSUE_ID_CONST + '/timetracking/workitem'
    ISSUE_URL = YOUTRACK_URL + '/rest/issue/' + ISSUE_ID_CONST
