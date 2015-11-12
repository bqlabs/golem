# coding=utf-8


import os


golem_file = os.path.join(os.path.expanduser('~'), "golem.txt")
print golem_file

class Golem(object):
    def __init__(self):
        if os.path.exists(golem_file):
            self._name = self.name
        else:
            self._name = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, _name):
        with open(golem_file, 'wb') as f:
            print _name
            f.write(_name)
        self._name = _name
