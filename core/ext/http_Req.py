import requests
from core.appConfig import AppConfigurations

config = AppConfigurations()


class RequestDispatcher:
    @staticmethod
    def MakeRequest(target: str, json=False, headers=None):
        if headers is None:
            headers = dict()
        try:
            req = requests.get(target, headers=headers)
            if req.status_code == 200:
                if json:
                    return req.json()
                return req.text
        except BaseException as e:

            config.debug(level=1, data=e)
