import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd
import os

st.set_page_config(layout="wide")
st.title("😃 Mood Survey - Speedometer Style")

# Mood options with corresponding values
moods = {
    "Very Sad 😞": 0,
    "Sad 🙁": 25,
    "Neutral 😐": 50,
    "Happy 🙂": 75,
    "Very Happy 😃": 100
}

# Mood ranges and colors
steps = [
    {'range': [0, 20], 'color': '#ff4b4b'},
    {'range': [20, 40], 'color': '#ffa500'},
    {'range': [40, 60], 'color': '#ffff00'},
    {'range': [60, 80], 'color': '#90ee90'},
    {'range': [80, 100], 'color': '#32CD32'}
]

# Function to create the speedometer
def create_speedometer(value, mood_label):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': f"<b>{mood_label}</b>", 'font': {'size': 30}},
        gauge = {
            'axis': {'range': [0, 100], 'startangle': -90, 'endangle': 90},
            'bar': {'color': "black", 'thickness': 0.25},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': steps,
            'threshold': {
                'line': {'color': "black", 'width': 8},
                'thickness': 0.75,
                'value': value
            }
        }
    ))

    fig.update_layout(
        margin=dict(t=20, b=0, l=0, r=0),
        paper_bgcolor="white",
        height=400
    )

    return fig

# Celebration animation
def celebrate_mood():
    st.success("🎉 Mood submitted successfully! 🎉")
    st.snow()
    st.markdown(
        "<div style='text-align: center; font-size:30px; color:green;'>🎊 Thank you for sharing your mood! 🎊</div>",
        unsafe_allow_html=True
    )

# Input name
name = st.text_input("Enter your name:")

# Mood selection
selected_mood = st.radio("How are you feeling today?", list(moods.keys()))

# Show speedometer
if selected_mood:
    mood_value = moods[selected_mood]
    mood_label = selected_mood.split()[0]
    
    if mood_label == "Very":
        mood_label = selected_mood.split()[1]
    
    fig = create_speedometer(mood_value, mood_label)
    st.plotly_chart(fig, use_container_width=True)

# Submit mood
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

        if os.path.exists("mood_responses_speedometer.xlsx"):
            existing_df = pd.read_excel("mood_responses_speedometer.xlsx")
            final_df = pd.concat([existing_df, df], ignore_index=True)
        else:
            final_df = df

        final_df.to_excel("mood_responses_speedometer.xlsx", index=False)

        celebrate_mood()
