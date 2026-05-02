import streamlit as st
import pickle
import pandas as pd

# ---------- LOAD MODEL ----------
model = pickle.load(open('model.pkl', 'rb'))

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Teen Depression Risk Predictor", layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
body { background-color: #0e1117; }
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 0px 15px rgba(0,0,0,0.5);
}
.title {
    text-align: center;
    font-size: 36px;
    font-weight: bold;
    color: white;
}
.subtitle {
    text-align: center;
    color: gray;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.sidebar.title("ℹ️ About")
st.sidebar.info("This app predicts depression risk in teens using lifestyle data.")

st.sidebar.markdown("### 📌 Tips")
st.sidebar.write("• Maintain good sleep")
st.sidebar.write("• Reduce stress")
st.sidebar.write("• Stay active")

st.markdown("<div class='title'>🧠 Teen Depression Risk Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Analyze lifestyle & predict depression risk in teens</div>", unsafe_allow_html=True)
st.markdown("---")

# ---------- LAYOUT ----------
col1, col2 = st.columns(2)

# ---------- INPUT SECTION ----------
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("👤 Personal & Lifestyle")

    age = st.number_input("Age", 13, 19, 16)
    gender = st.selectbox("Gender", ["Male", "Female"])
    social_media = st.slider("Social Media Hours", 0.0, 10.0, 3.0, step=0.5)

    platforms = st.multiselect(
        "Social Media Platforms",
        ["Instagram", "WhatsApp", "YouTube", "Snapchat", "Facebook", "Twitter"]
    )

    sleep = st.slider("Sleep Hours", 0.0, 12.0, 7.0, step=0.5)
    screen_time = st.slider("Screen Time Before Sleep", 0.0, 10.0, 2.0, step=0.5)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- HEALTH SECTION ----------
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("🧠 Health & Behavior")

    academic = st.slider("Academic Performance", 0.0, 10.0, 6.0, step=0.5)
    activity = st.slider("Physical Activity", 0.0, 10.0, 5.0, step=0.5)
    social = st.selectbox("Social Interaction", ["Low", "Medium", "High"])
    stress = st.slider("Stress Level", 0.0, 10.0, 5.0, step=0.5)
    anxiety = st.slider("Anxiety Level", 0.0, 10.0, 5.0, step=0.5)
    addiction = st.slider("Addiction Level", 0.0, 10.0, 3.0, step=0.5)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ---------- ENCODING ----------
gender = 1 if gender == "Male" else 0

num_platforms = len(platforms)
if num_platforms <= 1:
    platform_usage = 1
elif num_platforms == 2:
    platform_usage = 2
else:
    platform_usage = 0

social_map = {"Low": 0, "Medium": 1, "High": 2}
social = social_map[social]

if len(platforms) == 0:
    st.warning("⚠️ Please select at least one social media platform")

# ---------- PREDICTION ----------
if st.button("🚀 Predict Risk", use_container_width=True):

    data = pd.DataFrame([{
        'age': age,
        'gender': gender,
        'daily_social_media_hours': social_media,
        'platform_usage': platform_usage,
        'sleep_hours': sleep,
        'screen_time_before_sleep': screen_time,
        'academic_performance': academic,
        'physical_activity': activity,
        'social_interaction_level': social,
        'stress_level': stress,
        'anxiety_level': anxiety,
        'addiction_level': addiction
    }])

    # STEP 1: probability
    prob = model.predict_proba(data)[0][1]

    # STEP 2: override (ONLY ONCE)
    if stress >= 9 and anxiety >= 9 and sleep <= 4:
        prob = max(prob, 0.85)

    # STEP 3: prediction
    prediction = 1 if prob >= 0.5 else 0

    # STEP 4: risk band
    if prob < 0.3:
        band = "Low"
    elif prob < 0.7:
        band = "Moderate"
    else:
        band = "High"

    # DISPLAY (ALL INSIDE BLOCK)
    st.info(f"Risk Level: {band}")
    st.write(f"Probability: {prob:.2f}")

    # ---------- RESULT ----------
    st.markdown("## 📊 Result")

    if prediction == 1:
        st.error(f"⚠️ High Risk of Depression\n\nConfidence: {prob:.2f}")
        st.progress(int(prob * 100))

        st.markdown("### 🧠 Suggested Actions")

        if sleep < 6:
            st.write("😴 Improve sleep (7–9 hours)")
        if stress > 7:
            st.write("🧘 Manage stress")
        if anxiety > 7:
            st.write("💬 Talk to someone")
        if social_media > 6:
            st.write("📵 Reduce social media")
        if activity < 3:
            st.write("🏃 Increase physical activity")

        st.warning("⚠️ This is an AI-based prediction and not a medical diagnosis.")

    else:
        st.success(f"✅ Low Risk\n\nConfidence: {1-prob:.2f}")
        st.progress(int(prob * 100))

        st.markdown("### 👍 Maintain Healthy Habits")
        st.write("😴 Maintain good sleep")
        st.write("🏃 Stay active")
        st.write("📱 Use social media wisely")

    # ---------- EXPLANATION ----------
    st.markdown("### 🔍 Key Factors")

    if stress > 7:
        st.write("• High stress detected")
    if anxiety > 7:
        st.write("• High anxiety detected")
    if sleep < 5:
        st.write("• Poor sleep pattern")
    if social_media > 6:
        st.write("• Excessive social media usage")
    if activity < 3:
        st.write("• Low physical activity")
# ---------- FOOTER ----------
st.markdown("---")
st.markdown("<center>Created by Aayush Ingle ❤️</center>", unsafe_allow_html=True)