# -*- coding: utf-8 -*-
import os
import json
from os.path import exists, expanduser, join
from errno import EEXIST

from pycookiecheat import chrome_cookies

DEFAULT_ZIPLINE_ROOT = "~/.zipline"
XQ_URL = "https://xueqiu.com/"


def zipline_root():
    root = os.environ.get("ZIPLINE_ROOT", None)
    if root is None:
        root = expanduser(DEFAULT_ZIPLINE_ROOT)
    return root


def ensure_directory(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == EEXIST and os.path.isdir(path):
            return
        raise


def load_cookies():
    cookies = {}

    root = zipline_root()

    cookies_path = join(root, "cookies")
    if not exists(cookies_path):
        return cookies

    with open(cookies_path, "r") as f:
        cookies = json.load(f)
    return cookies


def refresh_cookies():
    cookies = chrome_cookies(XQ_URL)

    root = zipline_root()
    ensure_directory(root)

    cookies_path = join(root, "cookies")
    with open(cookies_path, "w+") as f:
        json.dump(cookies, f)
