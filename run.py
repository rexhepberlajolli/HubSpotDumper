# encoding: utf-8

from dumper.dumper import Dumper
import sys
import os
from collections import OrderedDict
import json

selectors = {
    'post_title': '//span[@id="hs_cos_wrapper_name"]',
    'author_name': '//span/a[@class="author-link"]',
    'excerpt': '(//span[@id="hs_cos_wrapper_post_body"]/p/strong)[1]',
    'post_html': '//span[@id="hs_cos_wrapper_post_body"]/node()[position()>1]',
    'about': '//div[@class="span10"]/p',
    'author_thumbnail': '//div[@class="span2"]/img/@src',
    'post_image': '//a[@class="hs-featured-image-link"]/img/@src',
    'post_keywords': '//a[@class="topic-link"]'
}


def main(_file):
    filename = _file.decode('utf-8')
    _file = Dumper(os.path.join(source, filename))
    for selector, xpath in selectors.items():
        _file.set_selector({selector: xpath})
    json_data = OrderedDict([
        ('post_title', _file.get_text('post_title')),
        ('author_name', _file.get_text('author_name')),
        ('excerpt', _file.get_html('excerpt')),
        ('post_html', _file.get_html('post_html')),
        ('about', _file.get_text('about')),
        ('author_thumbnail', _file.save_image('author_thumbnail',
                                              os.path.join(images_folder,
                                                           filename.split('.')[0]+'-author.jpg'))),
        ('post_image', _file.save_image('post_image',
                                        os.path.join(images_folder,
                                                     filename.split('.')[0]+'-post.jpg'))),
        ('post_keywords', _file.get_list('post_keywords'))])
    return {filename: json_data}


if __name__ == '__main__':
    if len(sys.argv) == 3:
        all_source_files = os.listdir(sys.argv[1])
        images_folder = os.path.join(sys.argv[2], 'images')
        data_json_file = os.path.join(sys.argv[2], 'data.json')
        if os.path.exists(os.path.join(sys.argv[2], 'images')):
            os.rmdir(os.path.join(sys.argv[2], 'images'))

        os.remove(data_json_file) if os.path.exists(images_folder) else None
        data = map(main, all_source_files[0])
        json_file = open(data_json_file, 'wb')
        json_file.write(json.dumps(data, indent=4))
        json_file.close()
    else:
        print "./run.py source target"
        print "example ./run.py /home/rexhep/hubspot/ /home/rexhep/hubspot_json/"
        sys.exit(1)
