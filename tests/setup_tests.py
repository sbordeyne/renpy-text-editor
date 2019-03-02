import sys
import os

sys.path.append(os.path.join(os.getcwd(), ".."))
os.chdir(os.path.join(os.getcwd(), ".."))
from RTE.config import config

class TestWM():
    def destroy(self):
        pass

class TestController():
    def __init__(self):
        self.options_wm = TestWM()
        pass


# os.system('xset r off')
