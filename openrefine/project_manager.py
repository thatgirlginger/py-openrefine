import requests

from connect import ServerConnection, ExistingProject #not sure if i actually need that first one
from exceptions import ProjectDoesNotExistError

class ProjectMetadata(ExistingProject):
    def __init__(self, pid):
        super().__init__(pid)
        self.csrf = self._get_token()