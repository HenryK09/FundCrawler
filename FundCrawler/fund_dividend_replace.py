import pandas as pd
import requests
import numpy as np
import os
import matplotlib. pyplot as plt


FILENAME = 'fund_price_change.csv'


def load_data():
    if os.path.isfile(FILENAME):
        fund_pricechg_df = load_fund_price()
    else:
        fund_pricechg_df = crawling()
        #to_csv()

    return fund_pricechg_df


def crawling():
    url = 'https://dis.kofia.or.kr/proframeWeb/XMLSERVICES/'

    xml_str = f"""<?xml version="1.0" encoding="utf-8"?>
    <message>
      <proframeHeader>
        <pfmAppName>FS-DIS2</pfmAppName>
        <pfmSvcName>DISFundStdPrcStutSO</pfmSvcName>
        <pfmFnName>select</pfmFnName>
      </proframeHeader>
      <systemHeader></systemHeader>
        <DISCondFuncDTO>
        <tmpV30>20000101</tmpV30>
        <tmpV31>20220125</tmpV31>
        <tmpV10>0</tmpV10>
        <tmpV12>KR5203318948</tmpV12>
    </DISCondFuncDTO>
    </message>"""

    headers = {
        'Accept': 'text/xml',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'text/xml',
        'Host': 'dis.kofia.or.kr',
        'Origin': 'https://dis.kofia.or.kr',
        'Referer': 'https://dis.kofia.or.kr/websquare/index.jsp?w2xPath=/wq/fundann/DISFundStdPrcStut.xml&divisionId=MDIS01004002000000&serviceId=SDIS01004002000',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
    }

    res = requests.post(url, data=xml_str, headers=headers).text

    fund_pricechg_df = pd.read_xml(res, xpath='.//selectMeta')

    fund_pricechg_df = fund_pricechg_df.loc[:, 'tmpV1':'tmpV12']

    fund_pricechg_df = fund_pricechg_df.rename(
        columns={'tmpV1': '기준일자',
                 'tmpV2': '기준가격',
                 'tmpV3': '전일대비등락(원)',
                 'tmpV4': '과표기준가격(원)',
                 'tmpV5': '설정원본(백만원)',
                 'tmpV6': 'KOSPI(P)',
                 'tmpV7': '국채금리(%)',
                 'tmpV8': '회사채금리(%)',
                 'tmpV9': '콜금리(%)',
                 'tmpV10': 'CP금리(%)',
                 'tmpV11': '투자운용인력',
                 'tmpV12': '표준코드'}
    )
    return fund_pricechg_df

# def to_csv():
#     fund_pricechg_df.to_csv('C:/Users/user/Desktop/fund_price_change.csv', encoding='utf-8-sig')

def load_fund_price():
    fund_price_change = pd.read_csv('C:/Users/user/Desktop/fund_price_change.csv', encoding='utf-8-sig')

    return fund_price_change

def load_dividend():

    divi_df = pd.read_csv('C:/Users/user/Desktop/dividend/divi.csv', encoding='utf-8-sig')
    divi_df['회계기말'] = pd.to_datetime(divi_df['회계기말'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
    divi_df = divi_df.set_index('회계기말')
    divi_df.index = pd.to_datetime(divi_df.index)
    divi_df = divi_df.reset_index()

    return divi_df


load_data()
#to_csv()
fund_price_change = load_fund_price()
divi_df =load_dividend()


fund_df = fund_price_change.sort_values('기준일자', ascending=True)
fund_df['기준일자'] = pd.to_datetime(fund_df['기준일자'], format='%Y%m%d')

fund_df = fund_df.set_index('기준일자')
fund_df = fund_df.reindex(pd.date_range(start='20010401', end='20220125'))

fund_df = fund_df.reset_index().rename(columns={'index':'기준일자'})
fund_df = pd.merge(fund_df, divi_df['분배율']/100, how='outer', left_on=fund_df['기준일자'], right_on=divi_df['회계기말'])
fund_df = fund_df.drop(columns='key_0').set_index('기준일자')

fund_df = fund_df[['기준가격','분배율']]
fund_df['분배율'] = fund_df['분배율'].shift(1)


fund_mask = fund_df.copy()

price_sr = fund_mask['기준가격']
dividend_sr = fund_mask['분배율']

price_sr = price_sr.dropna()
dividend_sr = dividend_sr.replace(0, np.nan)
dividend_sr = dividend_sr.dropna()

index_list = list(sorted(set(price_sr.index.tolist()) | set(dividend_sr.index.tolist())))

fund_mask = fund_mask.reindex(index_list)
fund_mask['기준가격'] = fund_mask['기준가격'].fillna(1000)
fund_mask['일수익률'] = fund_mask['기준가격'].pct_change()
fund_mask['총변화율'] = fund_mask[['일수익률', '분배율']].sum(axis=1)

sr = (fund_mask['총변화율'] + 1)
sr.iloc[0] = 1000

fund_mask['수정기준가'] = sr.cumprod()

plt.plot(fund_mask['수정기준가'])

fixed_price = fund_mask.to_csv('C:/Users/user/Desktop/FixedPrice.csv')