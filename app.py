import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="학생부 성적 관리 시스템",
    page_icon="📚",
    layout="wide"
)

DATA_FILE = "grades.csv"

# 데이터 불러오기
if Path(DATA_FILE).exists():
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=[
        "학년","학기","과목","단위수","등급"
    ])

st.title("📚 학생부 성적 관리 시스템")

# 사이드바
st.sidebar.header("성적 입력")

grade_year = st.sidebar.selectbox(
    "학년",
    [1,2,3]
)

semester = st.sidebar.selectbox(
    "학기",
    [1,2]
)

subject = st.sidebar.text_input("과목명")

credit = st.sidebar.number_input(
    "이수단위",
    min_value=1,
    max_value=10,
    value=3
)

grade = st.sidebar.number_input(
    "등급",
    min_value=1.0,
    max_value=9.0,
    step=0.1
)

if st.sidebar.button("추가"):
    new_row = {
        "학년":grade_year,
        "학기":semester,
        "과목":subject,
        "단위수":credit,
        "등급":grade
    }

    df = pd.concat(
        [df, pd.DataFrame([new_row])],
        ignore_index=True
    )

    df.to_csv(DATA_FILE, index=False)
    st.success("저장 완료")
    st.rerun()

# 메트릭
if len(df) > 0:

    weighted_avg = (
        (df["등급"] * df["단위수"]).sum()
        / df["단위수"].sum()
    )

    best = df.loc[df["등급"].idxmin()]
    worst = df.loc[df["등급"].idxmax()]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "전체 평균 등급",
        round(weighted_avg, 2)
    )

    col2.metric(
        "최고 성적 과목",
        best["과목"]
    )

    col3.metric(
        "보완 필요 과목",
        worst["과목"]
    )

# 데이터 표
st.subheader("성적 데이터")

edited_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="dynamic"
)

# 저장
if st.button("변경사항 저장"):
    edited_df.to_csv(DATA_FILE, index=False)
    st.success("저장 완료")

# 학기별 평균
if len(df) > 0:

    st.subheader("학기별 평균 등급")

    semester_avg = (
        df.groupby(["학년","학기"])
        .apply(
            lambda x:
            (x["등급"]*x["단위수"]).sum()
            / x["단위수"].sum()
        )
        .reset_index(name="평균등급")
    )

    semester_avg["구분"] = (
        semester_avg["학년"].astype(str)
        + "-"
        + semester_avg["학기"].astype(str)
    )

    fig = px.line(
        semester_avg,
        x="구분",
        y="평균등급",
        markers=True,
        title="학기별 성적 추이"
    )

    fig.update_yaxes(
        autorange="reversed"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# 과목별 분석
if len(df) > 0:

    st.subheader("과목별 평균")

    subject_avg = (
        df.groupby("과목")["등급"]
        .mean()
        .reset_index()
    )

    fig2 = px.bar(
        subject_avg,
        x="과목",
        y="등급",
        title="과목별 평균 등급"
    )

    fig2.update_yaxes(
        autorange="reversed"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# CSV 다운로드
csv = df.to_csv(index=False)

st.download_button(
    "CSV 다운로드",
    csv,
    file_name="grades.csv",
    mime="text/csv"
)
