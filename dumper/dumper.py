#!/usr/bin/python2.7

from lxml import etree
import lxml
from urllib import urlretrieve


class Dumper(object):
    def __init__(self, _file, selectors=None):
        if selectors is None:
            selectors = {}
        self._file = etree.parse(open(_file, 'rb'), etree.HTMLParser())
        self.selectors = dict(selectors)

    def set_selector(self, selectors=None):
        if selectors is None:
            selectors = {}
        self.selectors = dict(self.selectors.items() + selectors.items())

    def get_text(self, attribute):
        if attribute in self.selectors:
            return self._file.xpath(self.selectors[attribute])[0].text
        return "Set the selector first"

    def get_html(self, attribute):
        if attribute in self.selectors:
            return "".join([etree.tostring(elem) for elem in self._file.xpath(self.selectors[attribute]) if isinstance(elem, lxml.etree._Element)])

    def get_list(self, attribute, delimeter):
        return "".join([i.text for i in self._file.xpath(self.selectors[attribute])]).split(delimeter)

    def save_image(self, attribute, file_name):
        urlretrieve(self._file.xpath(self.selectors[attribute])[0], file_name)
