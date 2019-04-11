# coding=utf-8
# https://dev.fitbit.com/docs/heart-rate/

import fitbit
import json
import gather_keys_oauth2 as Oauth2
import matplotlib.pyplot as plt
import numpy as np
# グラフ化に必要なものの準備
import matplotlib
import matplotlib.pyplot as plt

# データの扱いに必要なライブラリ
import pandas as pd

"""for OAuth2.0"""
USER_ID = ''
CLIENT_SECRET = ''

"""for obtaining Access-token and Refresh-token"""
server = Oauth2.OAuth2Server(USER_ID, CLIENT_SECRET)
server.browser_authorize()
print('FULL RESULTS = %s' % server.oauth.token)
print('ACCESS_TOKEN = %s' % server.oauth.token['access_token'])

ACCESS_TOKEN = server.oauth.token['access_token']
REFRESH_TOKEN = server.oauth.token['refresh_token']

"""Authorization"""
auth2_client = fitbit.Fitbit(USER_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN,
                             refresh_token=REFRESH_TOKEN)

"""Getting data"""
fitbit_stats = auth2_client.intraday_time_series('activities/heart', base_date='2016-12-26', detail_level='1min')

"""Output api result to json"""
# print('FB STATUS = %s' % json.dumps(fitbit_stats))

"""Getting only 'heartrate' and 'time'"""
stats = fitbit_stats['activities-heart-intraday']['dataset']

"""Timeseries data of Heartrate"""
f1 = open('dataHR-timeseries.txt', 'w')
f1.write("\"\",\"date\",\"value\"\n")
for var in range(0, len(stats)):
    f1.write(str(var))
    f1.write(",")
    f1.write(stats[var]['time'])
    f1.write(",")
    f1.write(str(stats[var]['value']))
    f1.write("\n")
f1.close()

"""Output graph"""
df_sample = pd.read_csv("dataHR-timeseries.txt", parse_dates=True, index_col=1)
df = df_sample.iloc[:, 1:]
graph = df.plot(y=['value'], figsize=(16, 4), alpha=3)
