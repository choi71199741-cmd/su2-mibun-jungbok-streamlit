import streamlit as st
import random

st.title("📘 미분 퀴즈 앱")
st.write("함수의 도함수를 맞춰보세요!")

# 문제 생성
def generate_problem():
    a = random.randint(1, 5)
    b = random.randint(-5, 5)
    c = random.randint(-5, 5)

    question = f"f(x) = {a}x² {'+' if b>=0 else ''}{b}x {'+' if c>=0 else ''}{c}"
    answer = f"{2*a}x {'+' if b>=0 else ''}{b}"

    return question, answer, a, b


# 선택지 생성
def generate_choices(correct, a, b):
    wrongs = set()

    while len(wrongs) < 3:
        fake_a = random.choice([a, a+1, a-1, a*2])
        fake_b = random.choice([b, b+1, b-1, b*2])
        wrong = f"{fake_a}x {'+' if fake_b>=0 else ''}{fake_b}"

        if wrong != correct:
            wrongs.add(wrong)

    choices = list(wrongs) + [correct]
    random.shuffle(choices)

    return choices


# 힌트
def give_hint(attempt, a, b):
    if attempt == 1:
        return "💡 힌트: x² → 2x"
    elif attempt == 2:
        return f"💡 힌트: {a}x² → {2*a}x"
    elif attempt == 3:
        return f"💡 힌트: x항 미분 → {b}"
    else:
        return "💡 정답 형태: 2ax + b"


# 세션 상태 초기화
if "problem" not in st.session_state:
    q, ans, a, b = generate_problem()
    st.session_state.problem = q
    st.session_state.answer = ans
    st.session_state.a = a
    st.session_state.b = b
    st.session_state.choices = generate_choices(ans, a, b)
    st.session_state.attempt = 0
    st.session_state.solved = False


st.subheader(st.session_state.problem)

choice = st.radio("정답을 선택하세요:", st.session_state.choices)

if st.button("제출"):
    st.session_state.attempt += 1

    if choice == st.session_state.answer:
        st.success(f"🎉 정답입니다! → {st.session_state.answer}")
        st.session_state.solved = True
    else:
        st.error("❌ 틀렸습니다")
        st.info(give_hint(st.session_state.attempt,
                          st.session_state.a,
                          st.session_state.b))

if st.button("다음 문제"):
    q, ans, a, b = generate_problem()
    st.session_state.problem = q
    st.session_state.answer = ans
    st.session_state.a = a
    st.session_state.b = b
    st.session_state.choices = generate_choices(ans, a, b)
    st.session_state.attempt = 0
    st.session_state.solved = False
