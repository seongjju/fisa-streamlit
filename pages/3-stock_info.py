import streamlit as st
import pandas as pd
import FinanceDataReader as fdr    # 삼성전자 -> 종목코드 알려주지 않음
import datetime
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO   # 바이너리 파일들을 읽고 쓸 때 사용하는 패키지
import plotly.graph_objects as go
import pandas as pd
# pip freeze > requirements.txt  # 현재 사용한 패키지를 파일로 남깁니다.
# pip install -r requirements.txt # 이 프로그램에 필요한 패키지들을 일괄적으로 설치합니다.
# caching
# 인자가 바뀌지 않는 함수 실행 결과를 저장 후 크롬의 임시 저장 폴더에 저장 후 재사용
@st.cache_data
def get_stock_info():
    base_url =  "http://kind.krx.co.kr/corpgeneral/corpList.do"
    method = "download"
    url = "{0}?method={1}".format(base_url, method)
    df = pd.read_html(url, header=0, encoding='cp949')[0]
    df['종목코드']= df['종목코드'].apply(lambda x: f"{x:06d}")
    df = df[['회사명','종목코드']]
    return df
def get_ticker_symbol(company_name):
    df = get_stock_info()
    code = df[df['회사명']==company_name]['종목코드'].values
    ticker_symbol = code[0]
    return ticker_symbol
with st.sidebar:
    stock_name = st.text_input('회사 이름을 입력하세요: ')
    today = datetime.datetime.now()
    jan_1 = datetime.date(today.year, 1, 1)
    dec_31 = datetime.date(today.year, 12, 31)
    date_range = st.date_input(
        "시작일과 종료일을 입력하세요",
        (jan_1, today),
        jan_1,
        today,
        format="YYYY.MM.DD",
    )
    accept = st.button('확인')
if accept:
    ticker_symbol = get_ticker_symbol(stock_name)
    start_p = date_range[0]
    end_p = date_range[1]
    df = fdr.DataReader(f'KRX:{ticker_symbol}', start_p, end_p)
    df.index = df.index.date
    st.subheader(f"[{stock_name}] 주가 데이터")
    st.dataframe(df.tail(7))
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
    st.plotly_chart(fig, use_container_width=True)
    excel_data = BytesIO()
    df.to_excel(excel_data)
    st.download_button("엑셀 파일 다운로드",
            excel_data, file_name='stock_data.xlsx')