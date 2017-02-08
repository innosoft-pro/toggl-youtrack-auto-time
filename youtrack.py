from config import YoutrackConfig
import requests
from lxml import etree


class YoutrackDataManager:
    def __init__(self):
        self.cookie = self._login()

    def _login(self):
        data = {
            'login': YoutrackConfig.LOGIN,
            'password': YoutrackConfig.PASS
        }
        headers = {
            'connection': 'keep-alive',
            'content-type': 'application/x-www-form-urlencoded'
        }

        result = requests.post(YoutrackConfig.LOGIN_URL, data=data, headers=headers)

        result.raise_for_status()
        return result.headers['set-cookie']

    def load_tasks_with_attributes(self, toggle_time_entries):
        """
        loads from youtrack all attributes of corresponding tasks: subsystems, tags, descriptions
        :param toggle_time_entries: list of time entries. Each entry contains toggl_id, youtrack_id,
        full_description, duration (sec).
        :return: dict. key is youtrack issue id (example - MMX-111), value is object that contains following data:
        subsystem: str
        tags: list of str
        name: str
        """
        pass

    def track_time(self, toggle_time_entries):
        """
        adds to corresponding youtrack tasks work items with corresponding durations
        :param toggle_time_entries: list of time entries. Each entry contains toggl_id, youtrack_id,
        full_description, duration (sec).
        """
        headers = {
            'cookie': self.cookie,
            'content-type': 'application/xml'
        }

        for time_entry in toggle_time_entries:
            youtrack_url = YoutrackConfig.WORKITEM_URL.replace(YoutrackConfig.ISSUE_ID_CONST, time_entry['youtrack_id'])

            work_item_xml = etree.Element('workItem')
            # multiplying by 1000 needed because despite the fact that youtrack said "we accepted epoch unix",
            # which is in seconds, it need time in milliseconds
            epoch_date_str = str(int(time_entry['start_time'].timestamp() * 1000))
            duration_minutes_str = str(time_entry['duration'] // 60)
            etree.SubElement(work_item_xml, 'date').text = epoch_date_str
            etree.SubElement(work_item_xml, 'duration').text = duration_minutes_str
            etree.SubElement(work_item_xml, 'description').text = ''

            data = etree.tostring(work_item_xml, encoding='unicode')

            result = requests.post(youtrack_url,
                                   data=data,
                                   headers=headers)
            if result.status_code == 201:
                print('time {0:s} minutes for issue {1:s} tracked successfully'.format(duration_minutes_str,
                                                                                       time_entry['full_description']))
            else:
                print('cannot track time {0:s} minutes for issue {1:s}. Response message: {2:s}'
                      .format(duration_minutes_str, time_entry['full_description'], result.text))
