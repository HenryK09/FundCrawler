import pandas as pd
import matplotlib. pyplot as plt


fixed_price_df = pd.read_csv('C:/Users/user/Desktop/FixedPrice.csv')
trading_df = pd.read_csv('C:/Users/user/Desktop/Trading.csv')

fp_df = fixed_price_df[['기준일자','수정기준가']]
tri_df = trading_df[['AsOfDate','TotalReturnIndex','AdjustedNAV']]

df = pd.merge(tri_df, fp_df, left_on='AsOfDate', right_on='기준일자')
df = df.drop(columns='기준일자').set_index('AsOfDate')

df['TR_pc'] = df['TotalReturnIndex'].pct_change()
df['FP_pc'] = df['수정기준가'].pct_change()
df['AdjNAV_pc'] = df['AdjustedNAV'].pct_change()

tr_sr = df['TR_pc']+1
fp_sr = df['FP_pc']+1
adjnav_sr = df['AdjNAV_pc']+1

tr_sr.iloc[0] = 1000
fp_sr.iloc[0] = 1000

df['TR'] = tr_sr.cumprod()
df['FP'] = fp_sr.cumprod()

df = df[['TR','FP']]

fig, ax = plt.subplots()
ax.plot(df['TR'], '--r', label='TotalReturn')
ax.plot(df['FP'], '-b', label='FixedPrice')
ax.axis('equal')
leg = ax.legend();