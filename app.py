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
    /* 카드 배경색이 밝으므로, 글자색을 검정으로 명시 */
    .term-card {
        background: #f8f9fa;
        color: #000;  /* 추가: 글자색을 검정으로 지정 */
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

# 의학 용어 데이터베이스 (총 180개)
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
            {"term": "Brainstem", "definition": "뇌간"},
            # 추가 5개
            {"term": "Frontal Lobe", "definition": "전두엽"},
            {"term": "Parietal Lobe", "definition": "두정엽"},
            {"term": "Temporal Lobe", "definition": "측두엽"},
            {"term": "Occipital Lobe", "definition": "후두엽"},
            {"term": "Basal Ganglia", "definition": "기저핵"}
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
            {"term": "Receptor", "definition": "수용체"},
            # 추가 5개
            {"term": "Hormone", "definition": "호르몬"},
            {"term": "Enzyme", "definition": "효소"},
            {"term": "pH Balance", "definition": "산-염기 균형"},
            {"term": "Thermoregulation", "definition": "체온 조절"},
            {"term": "Blood Pressure Regulation", "definition": "혈압 조절"}
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
            {"term": "Mucous Membrane", "definition": "점막"},
            # 추가 5개
            {"term": "Tendon", "definition": "힘줄"},
            {"term": "Ligament", "definition": "인대"},
            {"term": "Elastic Tissue", "definition": "탄력성 조직"},
            {"term": "Reticular Tissue", "definition": "그물 조직"},
            {"term": "Serous Membrane", "definition": "장막"}
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
            {"term": "Embolism", "definition": "색전증"},
            # 추가 5개
            {"term": "Cardiac Output", "definition": "심박출량"},
            {"term": "Cardiomyopathy", "definition": "심근병증"},
            {"term": "Valvular Heart Disease", "definition": "심장판막질환"},
            {"term": "Peripheral Vascular Disease", "definition": "말초혈관질환"},
            {"term": "Stroke Volume", "definition": "일회박출량"}
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
            {"term": "Lung Cancer", "definition": "폐암"},
            # 추가 5개
            {"term": "Chronic Bronchitis", "definition": "만성 기관지염"},
            {"term": "Laryngitis", "definition": "후두염"},
            {"term": "Bronchiectasis", "definition": "기관지확장증"},
            {"term": "Pulmonary Fibrosis", "definition": "폐섬유화증"},
            {"term": "Respiratory Distress Syndrome", "definition": "호흡곤란 증후군"}
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
            {"term": "Gallstone", "definition": "담석"},
            # 추가 5개
            {"term": "Gastroparesis", "definition": "위마비"},
            {"term": "Esophagitis", "definition": "식도염"},
            {"term": "Diverticulitis", "definition": "게실염"},
            {"term": "Gastroenteritis", "definition": "위장염"},
            {"term": "Hemorrhoids", "definition": "치질(치핵)"}
        ],
        "신경계": {
            "두뇌": [
                {"term": "Anencephaly", "definition": "무뇌증"},
                {"term": "Cerebral Palsy", "definition": "뇌성마비"},
                {"term": "Meningitis", "definition": "수막염"},
                {"term": "Brain Tumor", "definition": "뇌종양"},
                {"term": "Epilepsy", "definition": "간질"},
                {"term": "Encephalitis", "definition": "뇌염"},
                {"term": "Hydrocephalus", "definition": "수두증"},
                {"term": "Cerebral Hemorrhage", "definition": "뇌출혈"},
                {"term": "Multiple Sclerosis", "definition": "다발성 경화증"},
                {"term": "Brain Abscess", "definition": "뇌농양"},
                # 추가 5개
                {"term": "Parkinson's Disease", "definition": "파킨슨병"},
                {"term": "Alzheimer's Disease", "definition": "알츠하이머병"},
                {"term": "Subdural Hematoma", "definition": "경막하 혈종"},
                {"term": "Concussion", "definition": "뇌진탕"},
                {"term": "Transient Ischemic Attack", "definition": "일과성 허혈 발작"}
            ],
            "증상": [
                {"term": "Aphasia", "definition": "실어증"},
                {"term": "Apraxia", "definition": "실행증"},
                {"term": "Ataxia", "definition": "운동실조"},
                {"term": "Convulsion", "definition": "경련"},
                {"term": "Dizziness", "definition": "어지러움"},
                {"term": "Vertigo", "definition": "현기증"},
                {"term": "Coma", "definition": "혼수"},
                {"term": "Syncope", "definition": "실신"},
                {"term": "Neuralgia", "definition": "신경통"},
                {"term": "Paralysis", "definition": "마비"},
                # 추가 5개
                {"term": "Headache", "definition": "두통"},
                {"term": "Insomnia", "definition": "불면증"},
                {"term": "Neurogenic Shock", "definition": "신경인성 쇼크"},
                {"term": "Spasm", "definition": "근육 경련"},
                {"term": "Paresthesia", "definition": "감각 이상"}
            ]
        }
    },
    "이비인후과": {
        "귀": [
            {"term": "Otitis Media", "definition": "중이염"},
            {"term": "Tinnitus", "definition": "이명"},
            {"term": "Deafness", "definition": "난청"},
            {"term": "Labyrinthitis", "definition": "미로염"},
            {"term": "Acoustic Neuroma", "definition": "청신경종양"},
            {"term": "Otosclerosis", "definition": "이경화증"},
            {"term": "Vestibular Neuritis", "definition": "전정신경염"},
            {"term": "Meniere Disease", "definition": "메니에르병"},
            {"term": "Cochlear Implant", "definition": "인공와우"},
            {"term": "Presbycusis", "definition": "노인성난청"},
            # 추가 5개
            {"term": "Ear Barotrauma", "definition": "이압손상"},
            {"term": "Cholesteatoma", "definition": "진주종"},
            {"term": "Otorrhea", "definition": "이루(귀액)"},
            {"term": "Otalgia", "definition": "이통(귀 통증)"},
            {"term": "Perforated Eardrum", "definition": "고막 천공"}
        ],
        "코": [
            {"term": "Rhinitis", "definition": "비염"},
            {"term": "Sinusitis", "definition": "부비동염"},
            {"term": "Epistaxis", "definition": "비출혈"},
            {"term": "Nasal Polyp", "definition": "비강폴립"},
            {"term": "Deviated Septum", "definition": "비중격만곡증"},
            {"term": "Anosmia", "definition": "후각상실"},
            {"term": "Rhinorrhea", "definition": "콧물"},
            {"term": "Nasal Obstruction", "definition": "비강폐쇄"},
            {"term": "Allergic Rhinitis", "definition": "알레르기성 비염"},
            {"term": "Nasal Trauma", "definition": "비부외상"},
            # 추가 5개
            {"term": "Nasopharyngitis", "definition": "비인두염"},
            {"term": "Rhinosinusitis", "definition": "비부비동염"},
            {"term": "Hyposmia", "definition": "후각저하"},
            {"term": "Turbinate Hypertrophy", "definition": "코벌미비대"},
            {"term": "Foreign Body in Nose", "definition": "코 이물"}
        ]
    },
    "비뇨기과": {
        "신장": [
            {"term": "Nephritis", "definition": "신장염"},
            {"term": "Renal Failure", "definition": "신부전"},
            {"term": "Nephrotic Syndrome", "definition": "신증후군"},
            {"term": "Pyelonephritis", "definition": "신우신염"},
            {"term": "Hydronephrosis", "definition": "수신증"},
            {"term": "Renal Cyst", "definition": "신낭종"},
            {"term": "Glomerulonephritis", "definition": "사구체신염"},
            {"term": "Kidney Stone", "definition": "신장결석"},
            {"term": "Renal Cancer", "definition": "신장암"},
            {"term": "Polycystic Kidney", "definition": "다낭성신장"},
            # 추가 5개
            {"term": "Nephroblastoma", "definition": "신아세포종(윌름스 종양)"},
            {"term": "Renal Artery Stenosis", "definition": "신동맥협착증"},
            {"term": "Renal Colic", "definition": "신산통"},
            {"term": "Renal Hypertension", "definition": "신성고혈압"},
            {"term": "Renal Osteodystrophy", "definition": "신성골이영양증"}
        ],
        "방광": [
            {"term": "Cystitis", "definition": "방광염"},
            {"term": "Urinary Retention", "definition": "요저류"},
            {"term": "Incontinence", "definition": "요실금"},
            {"term": "Bladder Cancer", "definition": "방광암"},
            {"term": "Overactive Bladder", "definition": "과민성방광"},
            {"term": "Neurogenic Bladder", "definition": "신경인성방광"},
            {"term": "Urethritis", "definition": "요도염"},
            {"term": "Urinary Tract Infection", "definition": "요로감염"},
            {"term": "Bladder Stone", "definition": "방광결석"},
            {"term": "Interstitial Cystitis", "definition": "간질성방광염"},
            # 추가 5개
            {"term": "Bladder Neck Obstruction", "definition": "방광경부폐색"},
            {"term": "Bladder Fistula", "definition": "방광루"},
            {"term": "Bladder Diverticulum", "definition": "방광게실"},
            {"term": "Dysuria", "definition": "배뇨통"},
            {"term": "Benign Prostatic Hyperplasia", "definition": "양성 전립선 비대증(비뇨기과적 문제)"}
        ]
    }
}

# 중첩된 딕셔너리를 단일 리스트로 변환
def flatten_terms(nested_dict):
    flat_list = []
    for val in nested_dict.values():
        if isinstance(val, dict):
            flat_list.extend(flatten_terms(val))
        elif isinstance(val, list):
            flat_list.extend(val)
    return flat_list

medical_terms = flatten_terms(nested_terms)

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
    
    # 전체 진행률 표시
    progress = len(st.session_state.all_time_completed) / len(medical_terms)
    st.progress(progress)
    st.write(f"전체 진행률: {progress*100:.1f}% ({len(st.session_state.all_time_completed)}/{len(medical_terms)})")

    # 오늘의 학습 용어 선택 (6개)
    random.seed(int(selected_date.strftime("%Y%m%d")))
    remaining_terms = [term for term in medical_terms 
                      if term not in st.session_state.all_time_completed]
    # 남은 용어가 6개 미만이면 전체에서 다시 뽑도록 처리
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
    st.metric(
        "학습한 용어 수",
        f"{total_progress}/{total_terms}",
        f"{(total_progress/total_terms*100):.1f}%"
    )

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
