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
    def __init__(self):
        self.FilePath = config.TEMP_WIN_PATH

    @staticmethod
    def Is_Json(file: str):
        return file.split('.')[-1] == 'json'

    def ParseJson(self, file):
        try:
            with open(os.path.join(self.FilePath, file), 'r') as f:
                data = json.loads(f.read())
                print(data)
                f.close()
                os.remove(os.path.join(self.FilePath, file))
        except BaseException as e:
            print(e)

    def ReadJson(self):
        for root, folders, files in os.walk(self.FilePath):
            for file in files:
                if self.Is_Json(file):
                    self.ParseJson(file)

    def RemoveTempFiles(self):
        for root, folders, files in os.walk(self.FilePath):
            for file in files:
                if self.Is_Json(file):
                    self.ParseJson(file)
                    os.remove(os.path.join(self.FilePath,file))
