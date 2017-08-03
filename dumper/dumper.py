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
            text = self._file.xpath(self.selectors[attribute])
            if len(text) > 0:
                return u'{}'.format(text[0].text)
        return None

    def get_html(self, attribute):
        if attribute in self.selectors:
            post = self._file.xpath(self.selectors[attribute])
            if post:
                return "".join([etree.tostring(elem) for elem in post if isinstance(elem, lxml.etree._Element)])
        return None

    def get_list(self, attribute):
        return [i.text for i in self._file.xpath(self.selectors[attribute])]

    def save_image(self, attribute, file_name):
        while True:
            try:
                image_link = self._file.xpath(self.selectors[attribute])
                if len(image_link) > 0:
                    urlretrieve(image_link[0], file_name)
                    return file_name
                return None
            except Exception as e:
                print str(e)
                continue
            break
