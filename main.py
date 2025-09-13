import streamlit as st
import pandas as pd
import altair as alt
import os

# 제목
st.title("🌍 MBTI 유형별 국가 Top10 비율 시각화")

# 기본 데이터 경로
default_file = "countriesMBTI_16types.csv"

df = None

# 1️⃣ 기본 CSV 파일이 있으면 자동으로 불러오기
if os.path.exists(default_file):
    df = pd.read_csv(default_file)
    st.success(f"기본 데이터 파일 `{default_file}`을(를) 불러왔습니다.")
else:
    # 2️⃣ 없을 경우 업로드 파일 사용
    uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("업로드한 CSV 파일을 불러왔습니다.")

if df is not None:
    # MBTI 유형 리스트 (Country 제외)
    mbti_types = [col for col in df.columns if col != "Country"]

    # 선택 박스: MBTI 유형 고르기
    selected_mbti = st.selectbox("MBTI 유형을 선택하세요:", mbti_types)

    # 선택한 유형에서 상위 10개 국가 추출
    top10 = df[["Country", selected_mbti]].nlargest(10, selected_mbti)

    # 데이터프레임 보여주기
    st.subheader(f"{selected_mbti} 비율이 높은 국가 Top 10")
    st.dataframe(top10)

    # Altair 그래프
    chart = (
        alt.Chart(top10)
        .mark_bar()
        .encode(
            x=alt.X(selected_mbti, title="비율", 
                    scale=alt.Scale(domain=[0, top10[selected_mbti].max()*1.1])),
            y=alt.Y("Country", sort="-x", title="국가"),
            tooltip=["Country", selected_mbti]
        )
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)
else:
    st.info("CSV 데이터를 불러올 수 없습니다. 기본 파일이 없으면 업로드하세요.")
