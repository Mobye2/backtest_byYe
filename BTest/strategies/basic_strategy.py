import pandas as pd


def kd_passavation(data, x):  # kd值三日鈍化判斷
    if data.at[x, 'k'] > 0.8 and data.at[x-1, 'k'] > 0.8 and data.at[x-2, 'k'] > 0.8 and data.at[x-3, 'k'] < 0.8:
        kd = True
    else:
        kd = False
    return kd


def low_shadow(data, x, thres):  # 下影線 thres%判斷
    lowerprice = min(data.at[x, "開盤價"], data.at[x, "收盤價"])
    loshadow = (lowerprice - data.at[x, "最低價"]) / data.at[x, "開盤價"]
    thres = thres*0.01
    if loshadow > thres:
        shadow = True
    else:
        shadow = False
    return shadow


def up_shadow(data, x, thres):  # 上影線3%判斷
    higherprice = max(data.at[x, "開盤價"], data.at[x, "收盤價"])
    upshadow = (data.at[x, "最高價"]-higherprice) / data.at[x, "開盤價"]
    thres = thres*0.01
    if upshadow > thres:
        upshadowj = True
    else:
        upshadowj = False
    return upshadowj


def MAlowsupport(data, x):
    # 20MA有支撐
    if data.at[x-2, '20MA'] < data.at[x-2, '收盤價'] and data.at[x-1, '20MA'] < data.at[x-1, '收盤價'] and data.at[x, '最低價'] <= data.at[x, '20MA'] < data.at[x, '收盤價']:
        MAlowsupportJ = True
    else:
        MAlowsupportJ = False
    return MAlowsupportJ


def MApass(data, x):
    if data.at[x-2, '20MA'] > data.at[x-2, '收盤價'] and data.at[x-1, '20MA'] > data.at[x-1, '收盤價'] and data.at[x, '20MA'] < data.at[x, '收盤價']:
        MApassJ = True
    else:
        MApassJ = False
    return MApassJ


def MAGap(data, x):
    a = data.at[x, '20MA']-data.at[x, '5MA']
    return a


def MAcross(data, x, magapday):  # x為日期 n為20MA-5MA，由負轉正的追蹤日

    p = 0
    for i in range(0, magapday):
        if MAGap(data, x-i) < MAGap(data, x-i-1):
            p += 1
        else:
            break
    if MAGap(data, x-1) > 0 and MAGap(data, x) < 0:
        p += 1
    if p == magapday+1:
        MAGapJ = True
    else:
        MAGapJ = False
    return MAGapJ


def Cross(data, index, colume1, colume2, days):  # 連續days後交叉,colume1逐漸超越colume2
    judge = False
    if all(0 > (data.at[index-1, colume1]-data.at[index-1, colume2]) > (data.at[index-1-j, colume1]-data.at[index-1-j, colume2]) for j in range(1, days)) and data.at[index, colume1] > data.at[index, colume2]:
        judge = True
    return judge


def volume_explode(data: pd.DataFrame, index, multi):  # 大量交易，大於平均交易量multi倍
    ave_volume = data.loc[:index, 'Trading_Volume'].tail(40).mean()
    if data.at[index, "Trading_Volume"] > multi*ave_volume:  # 低於平均交易量的n倍
        explode = True
    else:
        explode = False
    return explode
