# coding=utf-8


import os
import re


default_golem_conf = '''
[golem]
name:
[user]
name:
[books]
libro primero: test
'''
golemfile_path = os.path.join(os.path.expanduser('~'), "golem.txt")
if not os.path.exists(default_golem_conf):
    with open(golemfile_path, "w+") as f:
        f.write(default_golem_conf)


class Golem(object):
    def __init__(self):
        with open(golemfile_path, "r") as f:
            config = f.read()
        self.info = ConfigParser(config, ['golem', 'books', 'user'])
        self.id = self.info.golem
        self.books = self.info.books
        self.user = self.info.user


class ConfigParser(object):
    def __init__(self, text, allowed_fields=None):
        self._sections = {}
        self._allowed_fields = allowed_fields or []
        pattern = re.compile("^\[([a-z_]{2,50})\]")
        current_lines = []
        for line in text.splitlines():
            line = line.strip()
            if not line or line[0] == '#':
                continue
            m = pattern.match(line)
            if m:
                group = m.group(1)
                if self._allowed_fields and group not in self._allowed_fields:
                    raise ParserException("ConfigParser: Unrecognized field '%s'" % group)
                current_lines = []
                self._sections[group] = current_lines
            else:
                current_lines.append(line)
        for key, value in self._sections.iteritems():
            self._sections[key] = ConfigSection(key, "\n".join(value))

    def __getattr__(self, name):
        if name in self._sections:
            return self._sections[name]
        else:
            if self._allowed_fields and name in self._allowed_fields:
                return ""
            else:
                raise ParserException("ConfigParser: Unrecognized field '%s'" % name)

    def __repr__(self):
        rep = []
        for key, value in self._sections.iteritems():
            rep.append('[' + key + ']')
            rep.append(value.__repr__())
        return '\n'.join(rep)


class ConfigSection(object):

    def __init__(self, section, text):
        self.section = section
        self._sections = {}
        for line in text.splitlines():
            key, value = line.split(':', 1)
            value = value.replace(' ', '') if value.startswith(' ') else value
            self._sections['_'.join(key.split(' '))] = value

    def __getattr__(self, key):
        if key in self._sections:
            return self._sections[key]
        return None

    def __repr__(self):
        rep = []
        for key, value in self._sections.iteritems():
            rep.append(key + ': ' + value)
        rep = '\n'.join(rep)
        return rep


class ParserException(Exception):
    pass
