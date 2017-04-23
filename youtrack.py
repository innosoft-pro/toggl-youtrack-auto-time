from configuration import YoutrackConfig
import requests
from lxml import etree


class YoutrackDataManager:
    def __init__(self):
        self.cookie = self._login()
        self.attributes = ['Subsystem', 'summary', 'Ревьюер']

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
        Subsystem: str
        tag: list of str
        summary: str
        Ревьюер: list of str
        """
        headers = {
            'cookie': self.cookie
        }

        result_items = {}

        for time_entry in toggle_time_entries:
            youtrack_url = YoutrackConfig.ISSUE_URL.replace(YoutrackConfig.ISSUE_ID_CONST, time_entry['youtrack_id'])
            result = requests.get(youtrack_url, headers=headers)

            if result.status_code != 200:
                print('cannot load tags for issue {0:s}. Response message: {1:s}'
                      .format(time_entry['youtrack_id'], result.text))
                continue

            result_items[time_entry['youtrack_id']] = {}
            result_items[time_entry['youtrack_id']]['tag'] = []

            xml_string = result.text
            issue_xml_tree = etree.fromstring(xml_string.encode())
            for item in issue_xml_tree:

                if 'name' in item.attrib.keys():
                    atr_name = item.attrib['name']
                    if atr_name in self.attributes:
                        subitems = item.getchildren()
                        vals = [subitem.text for subitem in subitems if subitem.tag == 'value']
                        if len(vals) == 1:
                            result_items[time_entry['youtrack_id']][atr_name] = vals[0]
                        elif len(vals) > 1:
                            result_items[time_entry['youtrack_id']][atr_name] = vals
                elif item.tag == 'tag':
                    result_items[time_entry['youtrack_id']]['tag'].append(item.text)

            if 'Звезда' in result_items[time_entry['youtrack_id']]['tag']:
                result_items[time_entry['youtrack_id']]['tag'].remove('Звезда')

        return result_items

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
