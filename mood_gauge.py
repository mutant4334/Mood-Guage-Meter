import streamlit as st
import json
import os
from streamlit_lottie import st_lottie
import matplotlib.pyplot as plt

MOOD_FILE = "moods_data.json"
MOODS = ["Happy", "Sad", "Neutral", "Angry", "Excited", "Anxious"]

# Load Lottie animation
def load_lottiefile(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_cradle = load_lottiefile("newtons_cradle.json")

# Initialize mood counts
if not os.path.exists(MOOD_FILE):
    with open(MOOD_FILE, "w") as f:
        json.dump({mood: 0 for mood in MOODS}, f)

# Load mood data
with open(MOOD_FILE, "r") as f:
    mood_data = json.load(f)

st.set_page_config(page_title="Mood Cradle", layout="centered")

st_lottie(lottie_cradle, speed=1, loop=True, height=250)
st.title("💫 Newton's Cradle Mood Survey")
st.markdown("Share your current **mood** anonymously and be part of the emotional ripple.")

selected_mood = st.radio("🧠 What's your mood right now?", MOODS)

if st.button("🎯 Submit Mood"):
    mood_data[selected_mood] += 1
    with open(MOOD_FILE, "w") as f:
        json.dump(mood_data, f)
    st.success("Your mood has been added to the cradle!")

# Plotting the mood graph
st.subheader("📊 Collective Mood Vibes")
fig, ax = plt.subplots()
ax.bar(mood_data.keys(), mood_data.values(), color='orange')
ax.set_ylabel("Responses")
ax.set_title("Current Mood Distribution")
st.pyplot(fig)
