import requests
import pandas as pd


def FundDividend(start, end):

    url = 'https://dis.kofia.or.kr/proframeWeb/XMLSERVICES/'

    xml_str = f"""<?xml version="1.0" encoding="utf-8"?>
    <message>
      <proframeHeader>
        <pfmAppName>FS-DIS2</pfmAppName>
        <pfmSvcName>DISFundRdmpSO</pfmSvcName>
        <pfmFnName>select</pfmFnName>
      </proframeHeader>
      <systemHeader></systemHeader>
        <DISCondFuncDTO>
        <tmpV30>{start}</tmpV30>
        <tmpV31>{end}</tmpV31>
        <tmpV12>대신성장중소형주증권투자신탁[주식](운용)</tmpV12>
        <tmpV3></tmpV3>
        <tmpV5></tmpV5>
        <tmpV4></tmpV4>
        <tmpV7></tmpV7>
    </DISCondFuncDTO>
    </message>"""

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'Cookie': '__smVisitorID=V4ubac3GJYX; JSESSIONID=IstccKJEEkxM1i05Plsw7WKaL9L1Kd7GwbYQYPHMRl5b3lbvpTWZhxZmubAp9aGU.ap1_servlet_kofiadisEngine; userGb=01; disTdMenu=%EA%B2%B0%EC%82%B0%20%EB%B0%8F%20%EC%83%81%ED%99%98%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundRdmp.xml%26divisionId%3DMDIS01004004000000%26serviceId%3DSDIS01004004000%7C%7C%ED%8E%80%EB%93%9C%20%EC%88%98%EC%9D%B5%EB%B9%84%EC%9A%A9%20%EA%B3%84%EC%82%B0%EA%B8%B0%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundcal%2FDISIdvFndSrch.xml%26divisionId%3DMDIS01014000000000%26serviceId%3DSDIS01014000000%7C%7C%ED%8E%80%EB%93%9C%EB%B9%84%EA%B5%90%EA%B2%80%EC%83%89%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Fcmpann%2FDISFundCmpSrch.xml%26divisionId%3DMDIS01008000000000%26serviceId%3DSDIS01008000000%7C%7C%ED%8E%80%EB%93%9C%EA%B3%B5%EC%8B%9C%EA%B2%80%EC%83%89%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundAnnSrch.xml%26divisionId%3DMDIS01001000000000%26serviceId%3DSDIS01001000000%7C%7C%EA%B8%B0%EC%A4%80%EA%B0%80%EA%B2%A9%EB%93%B1%EB%9D%BD%EB%A5%A0%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundStdPrcRate.xml%26divisionId%3DMDIS01004003000000%26serviceId%3DSDIS01004003000%7C%7C%EA%B8%B0%EC%A4%80%EA%B0%80%EA%B2%A9%EB%B3%80%EB%8F%99%EC%B6%94%EC%9D%B4%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundStdPrcStut.xml%26divisionId%3DMDIS01004002000000%26serviceId%3DSDIS01004002000%7C%7C%ED%8E%80%EB%93%9C%EA%B8%B0%EC%A4%80%EA%B0%80%EA%B2%A9%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundStdPrice.xml%26divisionId%3DMDIS01004001000000%26serviceId%3DSDIS01004001000%7C%7C%EA%B8%88%EC%9C%B5%ED%88%AC%EC%9E%90%ED%9A%8C%EC%82%AC%EA%B3%B5%EC%8B%9C%EA%B2%80%EC%83%89%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Fcompann%2FDISCompAnnSrch.xml%26divisionId%3DMDIS02001000000000%26serviceId%3DSDIS02001000000%7C%7C%EC%A3%BC%EC%8B%9D%EA%B1%B0%EB%9E%98%20%EC%88%98%EC%88%98%EB%A3%8C%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Fcompann%2FDISComdStockTrdCms.xml%26divisionId%3DMDIS02007002000000%26serviceId%3DSDIS02007002000%7C%7C%ED%8E%80%EB%93%9C%ED%91%9C%EC%A4%80%EC%BD%94%EB%93%9C%EC%A1%B0%ED%9A%8C%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Fetcann%2FDISFundStandardCD.xml%26divisionId%3DMDIS04003000000000%26serviceId%3DSDIS04003000000',
        'Host': 'dis.kofia.or.kr',
        'Origin': 'https://dis.kofia.or.kr',
        'Referer': 'https://dis.kofia.or.kr/websquare/index.jsp?w2xPath=/wq/fundann/DISFundRdmp.xml&divisionId=MDIS01004004000000&serviceId=SDIS01004004000'
    }

    res = requests.post(url, data=xml_str.encode('utf-8-sig'), headers=headers).text

    fund_dividend_df = pd.read_xml(res, xpath='.//selectMeta')

    fund_dividend_df = fund_dividend_df.loc[:, 'tmpV3':'tmpV11']

    fund_dividend_df = fund_dividend_df.rename(
        columns={'tmpV3':'회계기초',
                 'tmpV4':'회계기말',
                 'tmpV5':'경과일수',
                 'tmpV6':'설정원본(백만원)',
                 'tmpV7':'기준가격(원)_기준',
                 'tmpV8':'기준가격(원)_과표',
                 'tmpV9':'분배율',
                 'tmpV10':'구분',
                 'tmpV11':'표준코드'}
    )

    fund_dividend_df = fund_dividend_df.set_index(['표준코드', '회계기말'])
    fund_dividend_df = fund_dividend_df.sort_values('회계기말',ascending=True)
    fund_dividend_df['수익률'] = fund_dividend_df['기준가격(원)_기준'].pct_change().fillna()
    fund_dividend_df['총변화율'] = fund_dividend_df['분배율'].sum(fund_dividend_df['수익률'])
    fund_dividend_df['수정기준가'] = fund_dividend_df['기준가격(원)_기준'].iloc[0].cumprod(fund_dividend_df['총변화율'])

    return fund_dividend_df