#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path
from datetime import datetime
import logging
import time
import json

import pychromecast

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
sh = logging.StreamHandler()

# add ch to logger
logger.addHandler(sh)


def load_config(filename):
    f = open(path.join(path.abspath(path.dirname(__file__)), filename), 'r')
    if not f:
        logger.error('not found config: {}'.filename)
        exit()
    conf = json.load(f)

    return (conf)


def connect_googlehome(conf):
    ip_addr = conf.get('google_home').get('ip_addr')
    if ip_addr:
        googlehome = pychromecast.Chromecast(ip_addr)
    else:
        chromecasts = pychromecast.get_chromecasts()
        if len(chromecasts) == 0:
            logger.error('not found Chromecasts.')
            exit()

        name = conf.get('google_home').get('friendly_name')
        if name:
            googlehome = next(
                c for c in chromecasts if c.device.friendly_name == name)
        else:
            googlehome = chromecasts[0]

    if not googlehome.is_idle:
        googlehome.quit_app()
        time.sleep(3)

    logger.info("connect to {}:{}".format(
        googlehome.device.model_name, googlehome.device.friendly_name))

    return (googlehome)


def get_media_type(conf):
    t = conf.get('media_type')
    if not t:
        t = 'mp3'
        logger.info('no config of media_type. so, set dafault value "mp3".')

    return (t)


def get_source_url(conf):
    url = conf.get('mp3_urls').get(datetime.now().strftime('%H'))
    if not url:
        logger.error('cannot get url')

    return (url)


def main():
    conf = load_config('config.json')

    cast = connect_googlehome(conf)
    media_type = get_media_type(conf)
    mp3_url = get_source_url(conf)

    cast.wait()
    cast.media_controller.play_media(mp3_url, 'audio/{}'.format(media_type))
    cast.media_controller.block_until_active()


if __name__ == '__main__':
    main()
