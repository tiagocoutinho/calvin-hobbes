# -*- coding: utf-8 -*-
#
# This file is part of the calvin-hobbes-get project
#
# Copyright (c) 2017 Tiago Coutinho
# Distributed under the MIT license. See LICENSE for more info.

"""calvin and hobbes comic downloader"""

import os
import sys
import logging
import datetime
import functools

import gevent
import gevent.pool
import grequests
from requests.exceptions import ConnectionError

from bs4 import BeautifulSoup

__version__ = '0.0.1'

name = "calvinandhobbes"
site = 'http://www.gocomics.com/{0}'.format(name)

first = datetime.date(1985, 11, 18)
last = datetime.date.today()

def from_user_date(date):
    if isinstance(date, datetime.date):
        return date
    return datetime.date(*map(int, date.split('-')))

def idates(start=first, end=datetime.date.today(), step=datetime.timedelta(days=1)):
    start = from_user_date(start)
    end = from_user_date(end)
    date = start
    while date < end:
        yield date
        date += step

def get_pool(pool=None, size=5):
    return gevent.pool.Pool(size=size) if pool is None else pool

def get_url(url, retries=5):
    logging.info("Asking for %s...", url)
    req = None
    while retries:
        req = grequests.get(url).send()
        logging.info("Got %s...", url)
        if req.response is None:
            if hasattr(req, "exception"):
                if type(req.exception) == ConnectionError:
                    logging.warning('Failed to get %s (retries left=%d). Retrying...',
                                    url, retries)
                    retries -= 1
                    continue
            else:
                break
        else:
            break

    if req.response is None:
        logging.error('Failed to get %s (retries left=%d). Skipping...',
                      url, retries)
    return req

def get_url_content(url, retries=5):
    resp = get_url(url, retries=retries).response
    if resp is None:
        return resp
    return resp.content

def get_url_page(url, retries=5):
    resp = get_url_content(url, retries=retries)
    if resp is None:
        return resp
    return BeautifulSoup(resp, 'html.parser')

def get_page(n, retries=5):
    return get_url_page('{0}/{1}'.format(site,n), retries=retries)

def get_page_image_url(n, retries=5):
    return get_page(n, retries=retries).find(attrs={'class':'item-comic-image'}).img['src']

def process_page(page, out_dir="."):
    page_str = page.strftime('%Y/%m/%d')
    try:
        image_url = get_page_image_url(page_str)
    except:
        logging.error('Failed to get page %s', page, exc_info=1)
        return
    file_name = str(page)
    logging.info('Processing %s', file_name)
    path = os.path.abspath(out_dir)
    full_name = os.path.join(path, file_name)
    if os.path.exists(full_name):
        logging.warning("%s already exists. Skipping...", full_name)
        return
    image = get_url_content(image_url)
    if image is None:
        return
    if not os.path.isdir(path):
        os.makedirs(path)
    with open(full_name, mode="wb") as f:
        f.write(image)
    logging.info("Saved %s in %s", file_name, path)

def process(out_dir=".", pages=None, pool=None):
    pool = get_pool(pool)
    Task = functools.partial(pool.spawn, process_page,
                             out_dir=out_dir)
    pages = tuple(pages or idates())
    logging.info('Fetching pages [%s, %s] (parallel=%d)', pages[0], pages[-1], pool.size)
    tasks = map(Task, pages)
    gevent.joinall(tuple(tasks))

def __main():
    import sys
    import time
    import argparse
    start = time.time()
    parser = argparse.ArgumentParser(description='calvin-hobbes downloader', version=__version__)
    parser.add_argument('-o', '--output-dir', default='~/Downloads/calvin-hobbes')
    parser.add_argument('-s', '--start-date', default=first)
    parser.add_argument('-e', '--end-date', default=last)
    parser.add_argument('--max-parallel', default=5, type=int)
    logging.basicConfig(level=logging.INFO, format="%(levelname)-8s %(message)s")
    args = parser.parse_args()
    pages = idates(args.start_date, args.end_date)
    pool = get_pool(size=args.max_parallel)
    process(out_dir=os.path.expanduser(args.output_dir), pages=pages, pool=pool)
    logging.info('Took %ss', time.time()-start)

def main():
    try:
        __main()
    except KeyboardInterrupt:
        print('Ctrl-C pressed. Bailing out...')

if __name__ == "__main__":
    main()
