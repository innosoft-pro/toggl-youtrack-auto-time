
class YoutrackDataManager:
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
        :return: bool (success or not)
        """
        pass