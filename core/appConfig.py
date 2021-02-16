from datetime import datetime


class AppConfigurations:
    DEBUG = True
    REGISTER_ERROR = False

    def Error_Register(self, data):
        try:
            with open('errorlog', '+a') as f:
                f.writelines(data + '\n')
                f.close()
        except IOError:
            pass

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
