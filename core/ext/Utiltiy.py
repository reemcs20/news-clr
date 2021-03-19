import json
import os
from core.appConfig import AppConfigurations

config = AppConfigurations()


def write_json(path: os.path, name: str, data_file: dict) -> None:
    """Write results into JSON file

    Args:
        name ([str]): [The name of the file]
        data_file ([dict]): The data to be written
        :param data_file: dictionary object to be saved into json file
        :param name:  file name
        :param path: a path refers to current keyword path
    """
    try:

        with open(os.path.join(path, f'{name}.json'), '+w') as fp:
            json.dump(data_file, fp, indent=3, sort_keys=True)
            fn = os.path.join(path, f'{name}.json')
            config.debug(level=3, data=f"File {fn} has been created")
    except BaseException as e:
        config.debug(level=1, data="Error Writing json")
        config.debug(level=1, data=e)


class EchoResult:
    """
    a class to manipulate results by reading, removing and updating them.
    """

    def __init__(self):
        self.FilePath = config.EnvironmentPath()  # Current environment path
        self.AllNews = {}  # a dict to collect all news into one dict

    @staticmethod
    def Is_Json(file: str) -> bool:
        """
        check file if it is json file
        :param file: path object
        :return: True if file is json
        """
        return file.split('.')[-1] == 'json'

    def ParseJson(self, file: os.path) -> None:
        """
        Parse json file and write to the main news collector
        :param file: a json file from self.ReadJson function
        :return: None
        """
        try:
            # read file as binary
            with open(os.path.join(self.FilePath, file), 'r') as f:
                data = json.loads(f.read())  # read data as json
                if data:  # if data is json proceed
                    # unpacking data to key and value shape
                    key = list(data.items())[0][0]
                    value = list(data.items())[0][1]
                    self.AllNews.update({key: value})  # write data to all news collector
                f.close()  # close file
                self.RemoveTempFile(os.path.join(self.FilePath, file))  # delete file after reading
        except BaseException as e:
            print(e)

    def ReadJson(self):
        """
        read json file from temp folders
        :return:
        """
        for root, folders, files in os.walk(self.FilePath):  # read all files in config.EnvironmentPath()
            for file in files:
                if self.Is_Json(file):  # checks if the file is json
                    self.ParseJson(file)  # call ParseJson function

    def RemoveTempFile(self, file: os.path) -> bool:
        """

        :param file: a file path to remove it after reading it
        :return: True if the file deleted successfully otherwise False
        """
        deleted = False
        try:
            if os.path.exists(file):
                os.remove(os.path.join(self.FilePath, file))
                if True:
                    deleted = True  # change deleted state
            else:
                if config.DEBUG:
                    config.debug(level=1, data="File does not exist {}".format(file))
        except OSError as e:  # Catch errors if occur
            print(e)
        return deleted
