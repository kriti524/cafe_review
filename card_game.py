import streamlit as st
import time
import random

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Cafe Buzz",
    page_icon="🃏",
    layout="centered"
)

# ---------------- CSS (BACKGROUND + ANIMATIONS + CARDS) ----------------
st.markdown("""
<style>

/* Full page background */
.stApp {
    background: 
        linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)),
        url("https://images.unsplash.com/photo-1509042239860-f550ce710b93");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Progress bar */
.progress > div > div {
    background: linear-gradient(90deg, #ff4b4b, #ff914d);
}

/* Card container */
.card button {
    height: 140px;
    font-size: 20px;
    border-radius: 18px;
    background: white;
    border: 2px solid #eee;
    transition: all 0.3s ease;
    transform-style: preserve-3d;
}

/* Hover flip */
.card button:hover {
    transform: rotateY(8deg) scale(1.06);
    box-shadow: 0 16px 35px rgba(0,0,0,0.25);
}

/* Shoot effect */
.card button:focus {
    animation: shoot 0.35s ease forwards;
}

@keyframes shoot {
    0% { transform: scale(1); opacity: 1; }
    100% { transform: scale(1.5) translateY(-60px); opacity: 0; }
}

/* Disabled state */
button:disabled {
    opacity: 0.4;
    transform: none !important;
    box-shadow: none !important;
}

/* Text contrast improvement */
h1, h2, h3, h4, p, label {
    color: #ffffff;
}

</style>
""", unsafe_allow_html=True)

# ---------------- GAME DATA ----------------
STAGES = [
    {
        "question": "Pick a card:\n\nHow was your overall experience?",
        "key": "experience",
        "cards": {
            "🌟 Excellent": "excellent",
            "😊 Good": "good",
            "🤔 Average": "average"
        }
    },
    {
        "question": "Pick a card:\n\nHow was the menu variety?",
        "key": "variety",
        "cards": {
            "🍽️ Wide": "wide and impressive",
            "🙂 Decent": "decent",
            "😐 Limited": "limited"
        }
    },
    {
        "question": "Pick a card:\n\nHow did you find the pricing?",
        "key": "price",
        "cards": {
            "💰 Great Value": "great value for money",
            "⚖️ Fair": "fairly priced",
            "💸 Expensive": "a bit expensive"
        }
    },
    {
        "question": "Pick a card:\n\nHow was the service?",
        "key": "service",
        "cards": {
            "🙌 Excellent": "excellent",
            "🙂 Polite": "polite and helpful",
            "🐢 Slow": "slow at times"
        }
    },
    {
        "question": "Pick a card:\n\nHow was the ambience?",
        "key": "ambience",
        "cards": {
            "☕ Cozy": "cozy and welcoming",
            "🌿 Pleasant": "pleasant",
            "🪑 Basic": "simple and basic"
        }
    }
]

# ---------------- SESSION STATE ----------------
if "stage" not in st.session_state:
    st.session_state.stage = 0
    st.session_state.answers = {}
    st.session_state.lock = False

# ---------------- HEADER ----------------
st.title("🃏 Cafe Buzz")
st.caption("Tap instinctively — no thinking, just vibes")

# ---------------- PROGRESS ----------------
st.progress(st.session_state.stage / len(STAGES))

# ---------------- GAME LOOP ----------------
if st.session_state.stage < len(STAGES):
    stage = STAGES[st.session_state.stage]
    st.markdown(f"### {stage['question']}")

    cols = st.columns(len(stage["cards"]))

    for col, (label, value) in zip(cols, stage["cards"].items()):
        with col:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            clicked = st.button(
                label,
                use_container_width=True,
                disabled=st.session_state.lock
            )
            st.markdown('</div>', unsafe_allow_html=True)

            if clicked and not st.session_state.lock:
                st.session_state.lock = True
                st.session_state.answers[stage["key"]] = value

                st.toast("💥 Locked in!", icon=random.choice(["🃏", "✨", "🔥"]))
                time.sleep(0.35)

                st.session_state.stage += 1
                st.session_state.lock = False
                st.rerun()

# ---------------- FINAL REVIEW ----------------
else:
    st.balloons()
    st.success("🎉 Review complete! Thank you")

    review = (
        f"I had an {st.session_state.answers['experience']} experience at this café. "
        f"The menu variety was {st.session_state.answers['variety']}, "
        f"pricing felt {st.session_state.answers['price']}, "
        f"the service was {st.session_state.answers['service']}, "
        f"and the ambience was {st.session_state.answers['ambience']}. "
        f"Overall, it was a pleasant visit."
    )

    st.header("🏆 Your Review")
    st.text_area("Auto-generated review", review, height=220)

    if st.button("🔄 Play Again"):
        st.session_state.clear()
        st.rerun()
