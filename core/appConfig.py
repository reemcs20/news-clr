import os
from datetime import datetime


class AppConfigurations:
    DEBUG = True
    REGISTER_ERROR = False
    TEMP_WIN_PATH = r'C:\Users\PC\OneDrive\NewsCrawlers\core\temp'
    TEMP_LINUX_PATH = r"/root/NewsCrawlers/core/temp/"
    Env = 'win'

    @staticmethod
    def Error_Register(data):
        try:
            with open('error_log', '+a') as f:
                f.writelines(data + '\n')
                f.close()
        except IOError:
            pass

    def EnvironmentPath(self):
        if self.Env == 'linux':
            # checks path if exists or not and create it
            if not os.path.exists("/root/NewsCrawlers/core/temp/"):
                os.makedirs("/root/NewsCrawlers/core/temp/")
                return r"/root/NewsCrawlers/core/temp/"
            else:

                return r"/root/NewsCrawlers/core/temp/"

        else:
            if not os.path.exists(r'C:\Users\PC\OneDrive\NewsCrawlers\core\temp'):
                os.makedirs(r'C:\Users\PC\OneDrive\NewsCrawlers\core\temp')
                return r'C:\Users\PC\OneDrive\NewsCrawlers\core\temp'
            else:
                return r'C:\Users\PC\OneDrive\NewsCrawlers\core\temp'

    def debug(self, level, data):
        """A debugger for diagnose the crawler
        :param level: a leve of the debug:
            1: an ERROR level
            2: an WARNING level
            3: a TEST level
        :param data: the actual data from the crawler"""
        if self.DEBUG:
            if level == 1:
                print("[ERROR]: ", data)
                if self.REGISTER_ERROR:
                    self.Error_Register("ERROR[{}] {}".format(datetime.now(), data))

            elif level == 2:
                print("[WARNING]: ", data)
            else:
                print("DEBUGGER:", data)
        else:
            pass
