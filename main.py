import streamlit as st
import random
import textwrap
import streamlit.components.v1 as components

st.set_page_config(page_title="MBTI로 찾아보는 맞춤 수학 공부법", page_icon="🧠➕", layout="wide")

# --- Helper data ---
MBTIS = [
    'ISTJ','ISFJ','INFJ','INTJ',
    'ISTP','ISFP','INFP','INTP',
    'ESTP','ESFP','ENFP','ENTP',
    'ESTJ','ESFJ','ENFJ','ENTJ'
]

# Fun mascot (emoji) per MBTI group
MASCOTS = {
    'ISTJ': '🦉', 'ISFJ': '🐢', 'INFJ': '🦄', 'INTJ': '🧙‍♂️',
    'ISTP': '🛠️', 'ISFP': '🎨', 'INFP': '🌱', 'INTP': '🔬',
    'ESTP': '🏎️', 'ESFP': '🎉', 'ENFP': '🌈', 'ENTP': '💡',
    'ESTJ': '🏛️', 'ESFJ': '🫶', 'ENFJ': '🤝', 'ENTJ': '🚀'
}

# Core study method recommendations per MBTI (short + extended)
RECOMMENDATIONS = {
    'ISTJ': {
        'title': '체계적으로, 계획대로: 루틴형 공부법',
        'short': '일일 체크리스트와 오답노트 중심. 최소 30분 블록으로 공부하세요.',
        'steps': [
            '1) 주간 학습 목표 설정 (대단원별 2–3개 목표)',
            '2) 매일 30분 핵심 개념 복습 + 30분 문제풀이',
            '3) 오답노트를 날짜별로 관리',
            '4) 모의고사 유형 분석 (주 1회)'        ]
    },
    'ISFJ': {
        'title': '따뜻하게 지켜주는 스터디: 친구와 함께하는 복습',
        'short': '친구와 함께 스터디, 서로 가르치며 이해도를 높이세요.',
        'steps': [
            '1) 이해한 내용을 친구에게 5분간 설명하기',
            '2) 문제 풀이를 번갈아 가며 실습',
            '3) 쉬운 목표(오늘 3문제)로 꾸준함 유지',
            '4) 체크리스트와 보상 시스템 도입'
        ]
    },
    'INFJ': {
        'title': '의미 중심 학습: 스토리로 연결하는 수학',
        'short': '개념의 "이유"를 깊게 파고들어 자신만의 노트를 만드세요.',
        'steps': [
            '1) 개념별로 "왜"를 적어보는 노트 만들기',
            '2) 실생활 예시나 그림으로 개념 연결',
            '3) 어려운 문제는 단계별로 분해해서 정리',
            '4) 주 1회 긴 호흡의 복습 세션'
        ]
    },
    'INTJ': {
        'title': '효율 최우선: 목표-전략-검증 루프',
        'short': '문제 유형 분석을 바탕으로 약한 부분을 자동화하듯 개선하세요.',
        'steps': [
            '1) 상위 10개 유형 선정 후 문제 풀기',
            '2) 시간 제한을 두고 실전 감각 익히기',
            '3) 틀린 유형을 데이터로 모아 패턴 파악',
            '4) 솔루션을 템플릿화하여 재사용'
        ]
    },
    'ISTP': {
        'title': '실전형: 손으로 직접 풀어보는 기계적 연습',
        'short': '짧고 굵게 문제를 많이 풀어보며 감각을 익히세요.',
        'steps': [
            '1) 20분 집중 세션으로 많은 문제 풀기',
            '2) 정답의 "핵심 트릭"을 메모',
            '3) 풀이 방식 영상(1–3분)으로 복기',
            '4) 틀린 문제는 즉시 다시 풀기'
        ]
    },
    'ISFP': {
        'title': '감성적 창의 학습: 시각화 & 아트 노트',
        'short': '다이어그램과 컬러펜으로 시각적 노트를 만들면 이해와 기억이 빨라집니다.',
        'steps': [
            '1) 개념마다 한 페이지씩 컬러 노트 제작',
            '2) 주요 공식은 그림으로 연결',
            '3) 어려운 문제는 단계별로 색칠하며 해석',
            '4) 주 1회 자신만의 풀이 포스터 만들기'
        ]
    },
    'INFP': {
        'title': '자기주도 탐구형: 호기심으로 파고들기',
        'short': '흥미를 느끼는 주제를 중심으로 수학을 연결하면 몰입이 잘됩니다.',
        'steps': [
            '1) 흥미 주제를 정하고 관련 문제 찾아 풀기',
            '2) 개념을 스스로 다시 서술해보기',
            '3) 변형 문제를 만들어 해결해보기',
            '4) 목표는 작게, 보상은 크게'
        ]
    },
    'INTP': {
        'title': '논리적 탐구형: 원리 중심 집중 학습',
        'short': '정의와 증명을 직접 정리하며 개념의 연결 구조를 만드세요.',
        'steps': [
            '1) 주요 정리·정의의 증명 직접 써보기',
            '2) 개념 간 맵(마인드맵) 만들기',
            '3) 유형별 핵심 아이디어를 요약',
            '4) 틀린 문제의 수학적 원인 분석'
        ]
    },
    'ESTP': {
        'title': '속전속결 실전형: 타임어택 연습',
        'short': '타이머로 제한시간을 두고 실전과 같은 연습을 하세요.',
        'steps': [
            '1) 10문제 20분 타임어택',
            '2) 쉬운 문제는 빠르게 처리, 어려운 문제는 표시',
            '3) 오답은 5분 내 재도전',
            '4) 점수 기반 보상 시스템 도입'
        ]
    },
    'ESFP': {
        'title': '에너지 충전형: 게임화한 공부',
        'short': '문제 풀이를 미션처럼 만들어 보상을 연결하세요.',
        'steps': [
            '1) 오늘의 미션(예: 5문제 클리어) 설정',
            '2) 틀리면 리트라이, 맞추면 스티커 획득',
            '3) 친구와 점수 경쟁',
            '4) 실전 모의 테스트로 긴장감 유지'
        ]
    },
    'ENFP': {
        'title': '아이디어 폭발형: 토론·창의적 응용',
        'short': '문제를 창의적으로 변형하고 친구들과 토론하세요.',
        'steps': [
            '1) 기본 문제의 변형 문제 3개 만들기',
            '2) 풀이 아이디어를 서로 브레인스토밍',
            '3) 개념을 짧은 영상으로 요약해보기',
            '4) 프로젝트형 학습으로 연결'
        ]
    },
    'ENTP': {
        'title': '변형·응용형: 문제를 해킹하라',
        'short': '문제의 약점을 찾아 다양한 풀이법을 실험하세요.',
        'steps': [
            '1) 같은 문제를 3가지 방법으로 풀어보기',
            '2) 최단 풀이를 찾아 시간 절약 연습',
            '3) 복잡한 문제를 작은 서브문제로 분리',
            '4) 친구와 풀이 토론'
        ]
    },
    'ESTJ': {
        'title': '관리형: 스케줄+피드백 루프',
        'short': '주간 리뷰와 목표 기반 점검으로 성취도를 올리세요.',
        'steps': [
            '1) 주간 목표·일간 체크리스트 작성',
            '2) 매주 모의고사로 성장 체크',
            '3) 약한 단원은 2배 투자',
            '4) 멘토(선생님) 피드백 받기'
        ]
    },
    'ESFJ': {
        'title': '돌봄형: 스터디 커뮤니티 활용',
        'short': '한 팀을 만들어 서로 돕고 피드백하세요.',
        'steps': [
            '1) 작은 스터디 그룹 만들기',
            '2) 서로의 풀이를 리뷰해주기',
            '3) 역할 분담(문제 출제자/채점자)',
            '4) 보상과 이벤트로 동기 유지'
        ]
    },
    'ENFJ': {
        'title': '리더형: 가르치며 배우기',
        'short': '다른 사람에게 가르치면 이해도가 최고로 올라갑니다.',
        'steps': [
            '1) 핵심 개념을 10분 강의로 준비',
            '2) 친구에게 설명하고 질문 받기',
            '3) 피드백을 받아 노트 보완',
            '4) 정기 발표로 실력 검증'
        ]
    },
    'ENTJ': {
        'title': '전략형: 결과 중심 학습',
        'short': '목표 점수와 데드라인을 정해 전략적으로 공부하세요.',
        'steps': [
            '1) 목표 시험 점수 설정 및 역산 계획',
            '2) 약점 우선 순위화 및 집중 공략',
            '3) 일별 성과 지표로 관리',
            '4) 정기적으로 전략 재검토'
        ]
    }
}

# --- UI ---
# Left: Controls, Right: Result & fun characters
col1, col2 = st.columns([1,2])

with col1:
    st.header("너의 MBTI를 골라봐! ✨")
    mbti = st.selectbox("MBTI 유형 선택", MBTIS, index=10)
    st.write("또는 아래 버튼으로 무작위 선택")
    if st.button("무작위 MBTI 뽑기 🎲"):
        mbti = random.choice(MBTIS)
        st.success(f"뽑힌 MBTI: {mbti}")

    st.markdown("---")
    st.subheader("추가 설정")
    study_time = st.slider("하루 평균 공부 시간 (예상)", 10, 300, 60, step=10)
    prefer_group = st.radio("스터디 스타일 선호", ["혼자 집중", "친구와 함께", "혼합"], index=0)
    st.button("추천 생성하기")

with col2:
    # Animated header using HTML + CSS
    header_html = f"""
    <div style='display:flex;align-items:center;gap:16px'>
      <div style='font-size:64px; transform: translateY(0); animation: bob 2s infinite;'>
        {MASCOTS.get(mbti,'🧠')}
      </div>
      <div>
        <h1 style='margin:0'>{mbti} — {RECOMMENDATIONS[mbti]['title']}</h1>
        <p style='margin:4px 0 0 0;font-size:18px'>{RECOMMENDATIONS[mbti]['short']}</p>
      </div>
    </div>
    <style>
    @keyframes bob {0%{transform:translateY(0)}50%{transform:translateY(-10px)}100%{transform:translateY(0)}}
    </style>
    """
    st.markdown(header_html, unsafe_allow_html=True)

    st.write('')
    st.subheader('맞춤형 4주 학습 플랜 🗓️')

    # create a simple 4-week plan based on study_time and MBTI
    base_minutes = study_time
    plan_lines = []
    for week in range(1,5):
        minutes = int(base_minutes * (1 + (0.05 * (week-1))))
        p = f"Week {week}: 매일 {minutes}분 — {RECOMMENDATIONS[mbti]['title']} 핵심 실천"
        plan_lines.append(p)

    for line in plan_lines:
        st.info(line)

    st.write('')
    st.subheader('실전 팁 & 단계별 가이드')
    for step in RECOMMENDATIONS[mbti]['steps']:
        st.write('• ' + step)

    st.write('')
    st.subheader('캐릭터 스티커와 효과')
    # small interactive area with emoji "stickers"
    sticker_html = """
    <div style='display:flex;gap:12px;align-items:center'>
      <div style='text-align:center;'>
        <div style='font-size:48px; filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.2)); animation: pop 1.6s infinite;'>📘</div>
        <div>계획북</div>
      </div>
      <div style='text-align:center;'>
        <div style='font-size:48px; animation: spin 6s linear infinite;'>✏️</div>
        <div>플래너</div>
      </div>
      <div style='text-align:center;'>
        <div style='font-size:48px; animation: float 3s ease-in-out infinite;'>🎯</div>
        <div>목표</div>
      </div>
    </div>
    <style>
    @keyframes pop {0%{transform:scale(1)}50%{transform:scale(1.12)}100%{transform:scale(1)}}
    @keyframes spin {0%{transform:rotate(0)}100%{transform:rotate(360deg)}}
    @keyframes float {0%{transform:translateY(0)}50%{transform:translateY(-8px)}100%{transform:translateY(0)}}
    </style>
    """
    st.markdown(sticker_html, unsafe_allow_html=True)

    st.write('')
    st.subheader('나만의 체크리스트 만들기')
    # Generate a quick checklist
    checklist = [
        '오늘 핵심 개념 1개 요약하기',
        '문제 5문제 풀이 (기본문제 3 + 응용 2)',
        '오답노트 3문제 정리',
        '짧은 복습 10분'
    ]
    if prefer_group != '혼자 집중':
        checklist.append('스터디 파트너에게 오늘 배운 것 5분 설명하기')

    for item in checklist:
        st.checkbox(item)

    st.write('')
    st.subheader('복습 알림용 짧은 문구')
    prompt_text = f"{mbti} 스타일로: 오늘은 '{RECOMMENDATIONS[mbti]['short']}'을(를) 기억하자!"
    st.code(prompt_text)

    st.write('')
    st.subheader('다운로드/공유')
    export_text = f"MBTI: {mbti}\n플랜:\n" + "\n".join(plan_lines) + "\n\n팁:\n" + "\n".join(RECOMMENDATIONS[mbti]['steps'])
    st.download_button('학습계획 텍스트로 저장', data=export_text, file_name=f'{mbti}_math_plan.txt')

    # small interactive confetti when pressing celebrate
    if st.button('성공! 축하해 🎉'):
        components.html("""
        <script src='https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js'></script>
        <canvas id='confetti-canvas' style='position:fixed;pointer-events:none;top:0;left:0;width:100%;height:100%;z-index:999999;'></canvas>
        <script>
        var myCanvas = document.getElementById('confetti-canvas');
        confetti.create(myCanvas, {resize: true})({particleCount: 120, spread: 160});
        </script>
        """, height=200)

# Footer
st.markdown("---")
st.caption('앱은 교육용 예시이며, 개인 상황에 맞게 조정해서 사용하세요. — 만든이: ChatGPT')

# Small easter egg: show fun random study boost
if st.button('오늘의 동기부여 받기 ✨'):
    boosts = [
        '짧게라도 매일 하면 실력이 쌓여요 — 15분부터 시작해보세요!',
        '틀린 문제 한 개를 정복하면 자신감이 생깁니다. 오늘 1개 정복!',
        '친구에게 오늘 배운 걸 설명해 보세요. 이해도가 확 올라갑니다.'
    ]
    st.balloons()
    st.success(random.choice(boosts))
