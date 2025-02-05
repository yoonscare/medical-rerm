import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import json
import plotly.graph_objects as go
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

# 의학 용어 데이터베이스
nested_terms = {
    "기초 의학": {
        "해부학": [
            {"term": "Cerebrum", "definition": "대뇌"},
            {"term": "Medulla Oblongata", "definition": "연수"},
            {"term": "Cerebellum", "definition": "소뇌"},
            {"term": "Hypothalamus", "definition": "시상하부"},
            {"term": "Thalamus", "definition": "시상"},
            {"term": "Pons", "definition": "뇌교"},
            {"term": "Hippocampus", "definition": "해마"},
            {"term": "Amygdala", "definition": "편도체"},
            {"term": "Corpus Callosum", "definition": "뇌량"},
            {"term": "Brainstem", "definition": "뇌간"}
        ],
        "생리학": [
            {"term": "Homeostasis", "definition": "항상성"},
            {"term": "Metabolism", "definition": "대사"},
            {"term": "Osmosis", "definition": "삼투"},
            {"term": "Diffusion", "definition": "확산"},
            {"term": "Active Transport", "definition": "능동수송"},
            {"term": "Membrane Potential", "definition": "막전위"},
            {"term": "Action Potential", "definition": "활동전위"},
            {"term": "Synapse", "definition": "시냅스"},
            {"term": "Neurotransmitter", "definition": "신경전달물질"},
            {"term": "Receptor", "definition": "수용체"}
        ],
        "조직학": [
            {"term": "Epithelium", "definition": "상피조직"},
            {"term": "Connective Tissue", "definition": "결합조직"},
            {"term": "Muscle Tissue", "definition": "근육조직"},
            {"term": "Nervous Tissue", "definition": "신경조직"},
            {"term": "Adipose Tissue", "definition": "지방조직"},
            {"term": "Cartilage", "definition": "연골"},
            {"term": "Bone Tissue", "definition": "골조직"},
            {"term": "Blood", "definition": "혈액"},
            {"term": "Lymphatic Tissue", "definition": "림프조직"},
            {"term": "Mucous Membrane", "definition": "점막"}
        ]
    },
    "임상 의학": {
        "순환기": [
            {"term": "Hypertension", "definition": "고혈압"},
            {"term": "Tachycardia", "definition": "빈맥"},
            {"term": "Bradycardia", "definition": "서맥"},
            {"term": "Arrhythmia", "definition": "부정맥"},
            {"term": "Myocardial Infarction", "definition": "심근경색"},
            {"term": "Angina Pectoris", "definition": "협심증"},
            {"term": "Heart Failure", "definition": "심부전"},
            {"term": "Atherosclerosis", "definition": "동맥경화증"},
            {"term": "Thrombosis", "definition": "혈전증"},
            {"term": "Embolism", "definition": "색전증"}
        ],
        "호흡기": [
            {"term": "Dyspnea", "definition": "호흡곤란"},
            {"term": "Bronchitis", "definition": "기관지염"},
            {"term": "Pneumonia", "definition": "폐렴"},
            {"term": "Emphysema", "definition": "폐기종"},
            {"term": "Asthma", "definition": "천식"},
            {"term": "Tuberculosis", "definition": "결핵"},
            {"term": "Pleurisy", "definition": "흉막염"},
            {"term": "Pneumothorax", "definition": "기흉"},
            {"term": "Pulmonary Edema", "definition": "폐부종"},
            {"term": "Lung Cancer", "definition": "폐암"}
        ],
        "소화기": [
            {"term": "Gastritis", "definition": "위염"},
            {"term": "Hepatitis", "definition": "간염"},
            {"term": "Cholecystitis", "definition": "담낭염"},
            {"term": "Pancreatitis", "definition": "췌장염"},
            {"term": "Appendicitis", "definition": "충수염"},
            {"term": "Cirrhosis", "definition": "간경변"},
            {"term": "Peptic Ulcer", "definition": "소화성 궤양"},
            {"term": "Crohn Disease", "definition": "크론병"},
            {"term": "Ulcerative Colitis", "definition": "궤양성 대장염"},
            {"term": "Gallstone", "definition": "담석"}
        ],
        "신경계": [
            {"term": "Meningitis", "definition": "수막염"},
            {"term": "Encephalitis", "definition": "뇌염"},
            {"term": "Stroke", "definition": "뇌졸중"},
            {"term": "Epilepsy", "definition": "간질"},
            {"term": "Parkinson Disease", "definition": "파킨슨병"},
            {"term": "Multiple Sclerosis", "definition": "다발성 경화증"},
            {"term": "Alzheimer Disease", "definition": "알츠하이머병"},
            {"term": "Migraine", "definition": "편두통"},
            {"term": "Brain Tumor", "definition": "뇌종양"},
            {"term": "Neuralgia", "definition": "신경통"}
        ]
    },
    "진단검사": {
        "혈액검사": [
            {"term": "Complete Blood Count", "definition": "전혈구검사"},
            {"term": "Hemoglobin", "definition": "헤모글로빈"},
            {"term": "Hematocrit", "definition": "적혈구용적률"},
            {"term": "White Blood Cell", "definition": "백혈구"},
            {"term": "Platelet", "definition": "혈소판"},
            {"term": "Erythrocyte Sedimentation Rate", "definition": "적혈구침강속도"},
            {"term": "Prothrombin Time", "definition": "프로트롬빈시간"},
            {"term": "Blood Glucose", "definition": "혈당"},
            {"term": "Blood Urea Nitrogen", "definition": "혈중요소질소"},
            {"term": "Creatinine", "definition": "크레아티닌"}
        ],
        "영상검사": [
            {"term": "X-ray", "definition": "엑스레이"},
            {"term": "CT Scan", "definition": "전산화단층촬영"},
            {"term": "MRI", "definition": "자기공명영상"},
            {"term": "Ultrasound", "definition": "초음파"},
            {"term": "PET Scan", "definition": "양전자방출단층촬영"},
            {"term": "Angiography", "definition": "혈관조영술"},
            {"term": "Mammography", "definition": "유방촬영술"},
            {"term": "Fluoroscopy", "definition": "투시검사"},
            {"term": "Bone Scan", "definition": "골스캔"},
            {"term": "Echocardiogram", "definition": "심장초음파"}
        ]
    }
}

# 중첩된 딕셔너리를 단일 리스트로 변환
medical_terms = []
for category in nested_terms.values():
    for subcategory in category.values():
        medical_terms.extend(subcategory)

# 세션 상태 초기화
if 'completed_terms' not in st.session_state:
    st.session_state.completed_terms = []
if 'monthly_completions' not in st.session_state:
    st.session_state.monthly_completions = 0
if 'all_time_completed' not in st.session_state:
    st.session_state.all_time_completed = []

# 사이드바 메뉴
with st.sidebar:
    menu_options = {
        "오늘의 학습": "book",
        "통계": "graph-up",
        "상품 시스템": "gift"
    }
    selected = option_menu(
        "학습 메뉴",
        list(menu_options.keys()),
        icons=list(menu_options.values()),
        menu_icon="cast",
        default_index=0,
    )

# 오늘의 학습 페이지
if selected == list(menu_options.keys())[0]:  # "오늘의 학습"
    st.title("🏥 오늘의 의학 용어")
    
    # 날짜 선택
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_date = st.date_input("학습 날짜 선택", datetime.now())
    
    # 진행률 표시
    progress = len(st.session_state.all_time_completed) / len(medical_terms)
    st.progress(progress)
    st.write(f"전체 진행률: {progress*100:.1f}% ({len(st.session_state.all_time_completed)}/{len(medical_terms)})")

    # 오늘의 학습 용어 선택 (6개)
    random.seed(int(selected_date.strftime("%Y%m%d")))
    remaining_terms = [term for term in medical_terms 
                      if term not in st.session_state.all_time_completed]
    today_terms = random.sample(remaining_terms if len(remaining_terms) >= 6 else medical_terms, 6)

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

# 통계 페이지
elif selected == list(menu_options.keys())[1]:  # "통계"
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

    # 전체 진행 현황
    st.subheader("전체 진행 현황")
    total_progress = len(st.session_state.all_time_completed)
    total_terms = len(medical_terms)
    st.metric("학습한 용어 수", f"{total_progress}/{total_terms}", 
              f"{(total_progress/total_terms*100):.1f}%")

# 상품 시스템 페이지
elif selected == list(menu_options.keys())[2]:  # "상품 시스템"
    st.title("🎁 상품 시스템")
    
    rewards = {
        10: "귀여운 메모지 세트",
        15: "프리미엄 노트",
        20: "스터디 플래너",
        25: "고급 만년필 세트",
        30: "프리미엄 학습 키트"
    }
    
    for count, reward in rewards.items():
        achieved = st.session_state.monthly_completions >= count
        container_class = "stats-card" if achieved else "term-card"
        status_text = "획득 완료! 🎉" if achieved else "아직 획득하지 못했습니다"
        
        st.markdown(f"""
        <div class="{container_class}">
            <h3>{count}회 완료 - {reward}</h3>
            <p>{status_text}</p>
        </div>
        """, unsafe_allow_html=True)

    # 현재 달성 현황
    current_completions = st.session_state.monthly_completions
    next_reward = next((count for count in sorted(rewards.keys()) 
                       if count > current_completions), None)
    if next_reward:
        remaining = next_reward - current_completions
        st.info(f"다음 상품까지 {remaining}회 남았습니다! 화이팅! 💪")

# 하단 정보
st.markdown("---")
st.markdown("Made with ❤️ for Medical Students")

# 모든 용어를 학습 완료했을 때 초기화 버튼
if len(st.session_state.all_time_completed) == len(medical_terms):
    st.success("🎓 축하합니다! 모든 의학 용어를 학습하셨습니다!")
    if st.button("처음부터 다시 시작하기"):
        st.session_state.all_time_completed = []
        st.session_state.completed_terms = []
        st.session_state.monthly_completions = 0
        st.experimental_rerun()
