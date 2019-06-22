from datetime import datetime


class Secret:
    key: str
    value: str
    tags: list
    parent_directory: str
    name: str
    description: str
    version: str
    encryption_key: str
    last_modified: datetime
    last_modified_user: str

    def __init__(self, key: str, value: str = None, tags: list = list, version: str = None, last_modified: datetime = None, last_modified_user: str = None,
                 description: str = '', encryption_key: str = None):
        self.key = key
        self.value = value
        self.tags = tags
        self.version = version
        self.last_modified = last_modified
        self.last_modified_user = last_modified_user
        self.description = description
        self.encryption_key = encryption_key

        result = key.split('/')
        self.parent_directory = result[1]
        self.name = result[2]
