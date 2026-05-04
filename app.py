import streamlit as st
import random

st.set_page_config(page_title="미분 퀴즈", page_icon="📘")

st.title("📘 미분 퀴즈 앱")
st.write("함수의 도함수를 맞춰보세요!")

# ------------------------
# 난이도 선택
# ------------------------
difficulty = st.selectbox("난이도 선택", ["쉬움", "보통", "어려움"])

# ------------------------
# 문제 생성
# ------------------------
def generate_problem(level):
    if level == "쉬움":
        a = random.randint(1, 5)
        b = 0
        c = random.randint(-5, 5)
        question_latex = f"{a}x^2 + {c}"
        answer = f"{2*a}x"

    elif level == "보통":
        a = random.randint(1, 5)
        b = random.randint(-5, 5)
        c = random.randint(-5, 5)
        question_latex = f"{a}x^2 + {b}x + {c}"
        answer = f"{2*a}x + {b}"

    else:  # 어려움
        a = random.randint(1, 3)
        b = random.randint(-3, 3)
        c = random.randint(-3, 3)
        d = random.randint(-3, 3)
        question_latex = f"{a}x^3 + {b}x^2 + {c}x + {d}"
        answer = f"{3*a}x^2 + {2*b}x + {c}"

    return question_latex, answer


# ------------------------
# 선택지 생성
# ------------------------
def generate_choices(correct):
    wrongs = set()

    while len(wrongs) < 3:
        fake = f"{random.randint(1,10)}x^{random.randint(1,2)} + {random.randint(-5,5)}"
        if fake != correct:
            wrongs.add(fake)

    choices = list(wrongs) + [correct]
    random.shuffle(choices)
    return choices


# ------------------------
# 힌트
# ------------------------
def give_hint(attempt):
    if attempt == 1:
        return "💡 x^n → nx^(n-1)"
    elif attempt == 2:
        return "💡 각 항을 따로 미분하세요"
    elif attempt == 3:
        return "💡 상수는 미분하면 0"
    else:
        return "💡 다시 계산해보세요!"


# ------------------------
# 세션 초기화
# ------------------------
if "problem" not in st.session_state:
    q, ans = generate_problem(difficulty)
    st.session_state.problem = q
    st.session_state.answer = ans
    st.session_state.choices = generate_choices(ans)
    st.session_state.attempt = 0


# ------------------------
# 문제 출력 (예쁜 수식)
# ------------------------
st.latex(f"f(x) = {st.session_state.problem}")

choice = st.radio("정답을 선택하세요:", st.session_state.choices)

if st.button("제출"):
    st.session_state.attempt += 1

    if choice == st.session_state.answer:
        st.success(f"🎉 정답! → {st.session_state.answer}")
    else:
        st.error("❌ 틀렸습니다")
        st.info(give_hint(st.session_state.attempt))


if st.button("다음 문제"):
    q, ans = generate_problem(difficulty)
    st.session_state.problem = q
    st.session_state.answer = ans
    st.session_state.choices = generate_choices(ans)
    st.session_state.attempt = 0
