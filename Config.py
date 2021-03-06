import os


def singleton(class_):
    """ The singleton decoration.

    Args:
        class_: the class to be decorated
    """
    instances = {}

    def getinstance():
        print('getting instance')
        if class_ not in instances:
            instances[class_] = class_()
        return instances[class_]

    return getinstance


@singleton
class Config:
    """ The configuration.

    Hard coded at this moment, may load from files later
    """
    def __init__(self):
        self.__src_dir = os.path.dirname(os.path.abspath(__file__))
        self.__style_path = 'file://' + self.__src_dir + '/res/style.css'
        self.__highlight_path = 'file://' + self.__src_dir + \
            '/res/highlight.css'
        self.__working_dir = os.getcwd()
        self.__mathjax_dir = 'file://' + self.__src_dir + \
            '/res/MathJax/MathJax.js'

    def get_src_dir(self):
        return self.__src_dir

    def get_style_path(self):
        return self.__style_path

    def get_highlight_path(self):
        return self.__highlight_path

    def get_working_dir(self):
        return self.__working_dir

    def get_mathjax_path(self):
        return self.__mathjax_dir


config = Config()
