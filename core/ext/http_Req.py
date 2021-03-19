import requests
from core.appConfig import AppConfigurations

config = AppConfigurations()


class RequestDispatcher:
    """
    a HTTP request dispatcher to avoid DRY concept and code redundancy
    """

    @staticmethod
    def MakeRequest(target: str, json=False, headers=None) -> str:
        """

        :param target: the actual URL to make request to
        :param json: boolean argument to tell the function the response is json
        :param headers: if true the headers will be shipped with request
        :return: text if not json otherwise json
        """
        if headers is None:  # ensure if there headers were supplied
            headers = dict()
        try:
            req = requests.get(target, headers=headers)  # send the request
            if req.status_code == 200:  # ensure request went successfully
                if json:  # is  the response in json type
                    return req.json() # return Response as Json object
                return req.text # return Response as string
        except BaseException as e:
            config.debug(level=1, data=e)
