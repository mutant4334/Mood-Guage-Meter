import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import os

st.set_page_config(layout="wide")
st.title("😃 Mood Survey - Likert Scale with Needle")

# Mood options with values
moods = {
    "Very Sad 😞": 1,
    "Sad 🙁": 2,
    "Neutral 😐": 3,
    "Happy 🙂": 4,
    "Very Happy 😃": 5
}

colors = ["#ff4b4b", "#ffa500", "#ffff00", "#90ee90", "#32CD32"]

# Function to create gauge with needle
def create_gauge(selected_mood_index, mood_text):
    fig = go.Figure()

    # Draw the semicircle (gauge background)
    fig.add_trace(go.Pie(
        values=[20] * 5 + [100],
        rotation=90,  # Start from bottom
        hole=0.6,
        marker_colors=colors + ["lightgray"],
        text=["Very Sad", "Sad", "Neutral", "Happy", "Very Happy", ""],
        direction="clockwise",
        sort=False,
        textinfo="none",
        hoverinfo="skip",
        showlegend=False
    ))

    # Draw the needle
    angle = (180 / 5) * (selected_mood_index - 1)  # Map 1-5 to 0°-180°
    angle_rad = np.deg2rad(angle)

    needle_length = 0.4
    x_center, y_center = 0.5, 0.5
    x_needle = x_center + needle_length * np.cos(np.pi - angle_rad)
    y_needle = y_center + needle_length * np.sin(np.pi - angle_rad)

    fig.add_trace(go.Scatter(
        x=[x_center, x_needle],
        y=[y_center, y_needle],
        mode="lines",
        line=dict(color="black", width=4),
        showlegend=False,
        hoverinfo="skip"
    ))

    # Central Mood Label
    fig.update_layout(
        annotations=[dict(
            x=0.5,
            y=0.3,
            text=f"<b>{mood_text}</b>",
            font=dict(size=30, color="gray"),
            showarrow=False
        )],
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor="lightgray",
        width=600,
        height=400
    )

    fig.update_traces(textfont_size=18)

    return fig

# Celebration animation
def celebrate_mood():
    st.success("🎉 Mood submitted successfully! 🎉")
    st.snow()
    st.markdown(
        "<div style='text-align: center; font-size:30px; color:green;'>🎊 Thank you for sharing your mood! 🎊</div>",
        unsafe_allow_html=True
    )

# Input Name
name = st.text_input("Enter your name:", "")

# Mood Selection
selected_mood = st.radio("How are you feeling today?", list(moods.keys()))

# Display gauge
if selected_mood:
    mood_index = moods[selected_mood]
    mood_label = selected_mood.split(' ')[0]  # remove emoji

    # Handle "Very Sad" and "Very Happy" better
    if mood_label == "Very":
        mood_label = selected_mood.split(' ')[1]

    fig = create_gauge(mood_index, mood_label)
    st.plotly_chart(fig, use_container_width=True)

# Submit button
if st.button("Submit Mood"):
    if name.strip() == "":
        st.error("⚠️ Please enter your name before submitting.")
    else:
        data = {
            "Timestamp": [datetime.now()],
            "Name": [name.strip()],
            "Mood": [selected_mood],
            "Emoji": [selected_mood.split()[-1]]
        }
        df = pd.DataFrame(data)

        if os.path.exists("mood_responses.xlsx"):
            existing_df = pd.read_excel("mood_responses.xlsx")
            final_df = pd.concat([existing_df, df], ignore_index=True)
        else:
            final_df = df

        final_df.to_excel("mood_responses.xlsx", index=False)

        celebrate_mood()
