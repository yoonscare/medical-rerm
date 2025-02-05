import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import json
import plotly.graph_objects as go
from streamlit_calendar import calendar
from streamlit_option_menu import option_menu
from streamlit_extras.card import card
import random

# ... (이전 코드와 동일한 페이지 설정 및 CSS)

# 확장된 의학 용어 데이터베이스
medical_terms = {
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
        ]
    }
}

# ... (중간 코드 생략)

# 오늘의 학습 용어 선택 (6개)
def get_daily_terms(date):
    # 날짜를 시드로 사용하여 랜덤 선택
    random.seed(int(date.strftime("%Y%m%d")))
    
    # 모든 용어를 하나의 리스트로 통합
    all_terms = []
    for category in medical_terms.values():
        for subcategory in category.values():
            all_terms.extend(subcategory)
    
    # 이미 완료한 용어 제외
    remaining_terms = [term for term in all_terms 
                      if term not in st.session_state.all_time_completed]
    
    # 남은 용어가 6개 미만이면 전체 용어에서 다시 선택
    if len(remaining_terms) < 6:
        remaining_terms = all_terms
    
    # 6개 용어 랜덤 선택
    return random.sample(remaining_terms, 6)

# 메인 페이지에서 사용
if selected == "오늘의 학습":
    # ... (이전 코드와 동일)
    
    # 선택된 날짜의 용어 가져오기
    today_terms = get_daily_terms(selected_date)
    
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

# ... (나머지 코드는 이전과 동일)

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
