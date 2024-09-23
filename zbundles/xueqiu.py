# -*- coding: utf-8 -*-
import os
import time
import logging

import numpy as np
import pandas as pd
import requests

from zbundles.utils import load_cookies

logger = logging.getLogger(__name__)

daily_kline_url_tpl = (
    "https://stock.xueqiu.com/v5/stock/chart/kline.json?"
    "symbol={}&begin={}&period=day&type=before&count={}&"
    "indicator=kline,market_capital"
)


def extract_symbols():
    env_data = os.environ.get("SYMBOLS", "")
    symbols = [s for s in env_data.split(",") if s.strip()]
    return set(symbols)


def create_metadata_df(num_symbols):
    return pd.DataFrame(np.empty(num_symbols, dtype=[
        ('start_date', 'datetime64[ns]'),
        ('end_date', 'datetime64[ns]'),
        ('auto_close_date', 'datetime64[ns]'),
        ('symbol', 'object'),
        ('exchange', 'object'),]))


def download_data(symbol, end_ms, bar_count, cookies):
    count = "-%d" % bar_count
    url = daily_kline_url_tpl.format(symbol, end_ms, count)
    logger.info(f"Downloading daily kline: {url}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    }
    resp = requests.get(url, cookies=cookies, headers=headers)
    results = resp.json()["data"]["item"]

    index = []
    records = []
    for result in results:
        date = pd.Timestamp(result[0], unit='ms').normalize()
        index.append(date)
        record = {
            "volume": result[1],
            "open": result[2],
            "high": result[3],
            "low": result[4],
            "close": result[5],
            # "traded_value": result[9],
        }
        records.append(record)
    df = pd.DataFrame.from_records(records, index=index)

    df['dividend'] = 0
    df['split'] = 1
    return df


def daily_data_generator(symbols, end_date, bar_count, metadata_df):
    exchange = "xueqiu"

    now = pd.Timestamp.now()
    if end_date > now:
        end_date = now
    end_ms = int(time.mktime(end_date.timetuple()) * 1000)

    # cookies = {
    #     "u": "",
    #     "xq_a_token": "",
    # }
    cookies = load_cookies()
    if not cookies:
        logger.warning("Cookies not found, please refresh cookies first")
        raise ValueError("Cookies not found")

    for idx, symbol in enumerate(symbols):
        data_df = download_data(symbol, end_ms, bar_count, cookies)
        start_date, end_date = data_df.index[0], data_df.index[-1]
        autoclose_date = end_date + pd.Timedelta(days=1)
        metadata_df.iloc[idx] = start_date, end_date, autoclose_date, symbol, exchange

        yield idx, data_df


def create_xueqiu_bundle(end_date, bar_count):
    def ingest(environ,
               asset_db_writer,
               minute_bar_writer,
               daily_bar_writer,
               adjustment_writer,
               calendar,
               start_session,
               end_session,
               cache,
               show_progress,
               output_dir):
        symbols = extract_symbols()
        if show_progress:
            logger.info(f"Symbols: {symbols}")

        metadata_df = create_metadata_df(len(symbols))

        data = daily_data_generator(symbols, end_date, bar_count, metadata_df)
        daily_bar_writer.write(data, show_progress=show_progress)

        asset_db_writer.write(equities=metadata_df)
        adjustment_writer.write()
    return ingest
