import datetime
import requests
import os

from exceptions import ConnectionError, ProjectDoesNotExistError 

class ServerConnection:
    def __init__(self, host='127.0.0.1', port=3333):
        self.base_url = f"http://{host}:{port}"
        self.existing_projects = "command/core/get-all-project-metadata"

    def _connect_to_openrefine(self):
        try:
            r = requests.get(url=self.base_url)
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Connection refused on current configuration. Is OpenRefine running on the host and port configured?")

    def _get_token(self):
        r = requests.get(f"{self.base_url}/command/core/get-csrf-token?project={self.pid}").json()
        return r['token']

    def list_projects(self):
        self._connect_to_openrefine()
        res_data = requests.get(url=f"{self.base_url}/{self.existing_projects}").json()
        return res_data['projects']

class ExistingProject(ServerConnection):
    '''
    defines attributes and methods for a given project id
    '''
    def __init__(self, pid):
        super().__init__()
        self.pid = pid
        self.project = self.list_projects()[self.pid]
        if not self.project:
            raise ProjectDoesNotExistError("The project does not exist; Are you using the correct project id?")
        self.name = self.project['name']
        self.created_date = self.project['created']
        self.modified_date = self.project['modified']
        self.creator = self.project['creator']
        self.description = self.project['description']
        self.tags = self.project['tags']
        self.contributors = self.project['contributors']
        self.subject = self.project['subject']
        self.rowcount = self.project['rowCount']

    def open_project(self):
        return requests.get(url=f"{self.base_url}/project?project={self.pid}")