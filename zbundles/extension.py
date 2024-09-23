# -*- coding: utf-8 -*-
import pandas as pd
from zipline.data.bundles import register

from zbundles import create_xueqiu_bundle


register(
    'xueqiu',
    create_xueqiu_bundle(
        end_date=pd.Timestamp.now(),
        bar_count=600,
    ),
    calendar_name='NYSE',
)
