import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import json
import plotly.graph_objects as go
from streamlit_calendar import calendar
from streamlit_option_menu import option_menu
from streamlit_extras.card import card
import random

# 페이지 설정
st.set_page_config(
    page_title="의학 용어 학습",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일 적용
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton > button {
        width: 100%;
        border-radius: 20px;
        height: 3rem;
        background: linear-gradient(45deg, #4F46E5, #7C3AED);
        color: white;
        font-weight: bold;
    }
    .term-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .stats-card {
        background: linear-gradient(45deg, #4F46E5, #7C3AED);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 확장된 의학 용어 데이터베이스
medical_terms = {
    "기초 의학": {
        "해부학": [
            {"term": "Cerebrum", "definition": "대뇌"},
            {"term": "Medulla Oblongata", "definition": "연수"},
            {"term": "Cerebellum", "definition": "소뇌"},
            {"term": "Hypothalamus", "definition": "시상하부"},
        ],
        "생리학": [
            {"term": "Homeostasis", "definition": "항상성"},
            {"term": "Metabolism", "definition": "대사"},
            {"term": "Osmosis", "definition": "삼투"},
            {"term": "Diffusion", "definition": "확산"},
        ]
    },
    "임상 의학": {
        "순환기": [
            {"term": "Hypertension", "definition": "고혈압"},
            {"term": "Tachycardia", "definition": "빈맥"},
            {"term": "Bradycardia", "definition": "서맥"},
            {"term": "Arrhythmia", "definition": "부정맥"},
        ],
        "호흡기": [
            {"term": "Dyspnea", "definition": "호흡곤란"},
            {"term": "Bronchitis", "definition": "기관지염"},
            {"term": "Pneumonia", "definition": "폐렴"},
            {"term": "Emphysema", "definition": "폐기종"},
        ],
        "소화기": [
            {"term": "Gastritis", "definition": "위염"},
            {"term": "Hepatitis", "definition": "간염"},
            {"term": "Cholecystitis", "definition": "담낭염"},
            {"term": "Pancreatitis", "definition": "췌장염"},
        ]
    },
    "진단검사": {
        "혈액검사": [
            {"term": "Hemoglobin", "definition": "헤모글로빈"},
            {"term": "Leukocyte", "definition": "백혈구"},
            {"term": "Platelet", "definition": "혈소판"},
            {"term": "Hematocrit", "definition": "적혈구용적"},
        ],
        "영상검사": [
            {"term": "MRI", "definition": "자기공명영상"},
            {"term": "CT", "definition": "전산화단층촬영"},
            {"term": "Ultrasound", "definition": "초음파"},
            {"term": "X-ray", "definition": "엑스레이"},
        ]
    }
}

# 세션 상태 초기화
if 'completed_terms' not in st.session_state:
    st.session_state.completed_terms = []
if 'monthly_completions' not in st.session_state:
    st.session_state.monthly_completions = 0
if 'all_time_completed' not in st.session_state:
    st.session_state.all_time_completed = []

# 사이드바 메뉴
with st.sidebar:
    selected = option_menu(
        "학습 메뉴",
        ["오늘의 학습", "통계", "상품 시스템"],
        icons=['book', 'graph-up', 'gift'],
        menu_icon="cast",
        default_index=0,
    )

# 메인 페이지
if selected == "오늘의 학습":
    st.title("🏥 오늘의 의학 용어")
    
    # 날짜 선택
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_date = st.date_input("학습 날짜 선택", datetime.now())
    
    # 진행률 표시
    total_terms = sum(len(subcat) for cat in medical_terms.values() 
                     for subcat in cat.values())
    progress = len(st.session_state.all_time_completed) / total_terms
    st.progress(progress)
    st.write(f"전체 진행률: {progress*100:.1f}% ({len(st.session_state.all_time_completed)}/{total_terms})")

    # 오늘의 학습 용어 선택 (6개)
    random.seed(int(selected_date.strftime("%Y%m%d")))
    today_terms = []
    for category in medical_terms.values():
        for subcategory in category.values():
            today_terms.extend(subcategory)
    today_terms = random.sample(today_terms, min(6, len(today_terms)))

    # 용어 카드 표시
    cols = st.columns(3)
    for idx, term in enumerate(today_terms):
        with cols[idx % 3]:
            card_key = f"term_card_{idx}"
            with st.container():
                st.markdown(f"""
                <div class="term-card">
                    <h3>{term['term']}</h3>
                    <p>{term['definition']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("완료", key=card_key):
                    if term not in st.session_state.completed_terms:
                        st.session_state.completed_terms.append(term)
                        st.session_state.all_time_completed.append(term)
                        st.session_state.monthly_completions += 1
                        st.success("잘 하셨습니다! 🎉")
                        st.balloons()

elif selected == "통계":
    st.title("📊 학습 통계")
    
    # 월간 완료 통계
    st.subheader("월간 완료 현황")
    monthly_data = pd.DataFrame({
        "완료 횟수": [st.session_state.monthly_completions],
        "목표": [30]
    })
    
    fig = go.Figure(data=[
        go.Bar(name="완료", y=monthly_data["완료 횟수"], marker_color="#4F46E5"),
        go.Bar(name="목표", y=monthly_data["목표"], marker_color="#7C3AED")
    ])
    
    fig.update_layout(
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

elif selected == "상품 시스템":
    st.title("🎁 상품 시스템")
    
    rewards = {
        10: "귀여운 메모지 세트",
        15: "프리미엄 노트",
        20: "스터디 플래너",
        25: "고급 만년필 세트",
        30: "프리미엄 학습 키트"
    }
    
    for count, reward in rewards.items():
        if st.session_state.monthly_completions >= count:
            st.markdown(f"""
            <div class="stats-card">
                <h3>{count}회 완료 - {reward}</h3>
                <p>획득 완료! 🎉</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="term-card">
                <h3>{count}회 완료 - {reward}</h3>
                <p>아직 획득하지 못했습니다</p>
            </div>
            """, unsafe_allow_html=True)

# 하단 정보
st.markdown("---")
st.markdown("Made with ❤️ for Medical Students")
