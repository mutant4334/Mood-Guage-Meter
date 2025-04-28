import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import os
from datetime import datetime

st.set_page_config(layout="wide")
st.title("😃 Mood Survey - Speedometer Style")

# Define moods with corresponding gauge values
moods = {
    "Very Sad": 10,
    "Sad": 30,
    "Neutral": 50,
    "Happy": 70,
    "Very Happy": 90
}

colors = ['#FF4B4B', '#FFA500', '#FFFF00', '#90EE90', '#32CD32']

# Function to create gauge
def create_gauge(value, mood_label):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        gauge={
            'shape': "semi",
            'axis': {'range': [0, 100]},
            'bar': {'color': "black", 'thickness': 0.3},
            'steps': [
                {'range': [0, 20], 'color': colors[0]},
                {'range': [20, 40], 'color': colors[1]},
                {'range': [40, 60], 'color': colors[2]},
                {'range': [60, 80], 'color': colors[3]},
                {'range': [80, 100], 'color': colors[4]},
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        },
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"<b>{mood_label}</b>", 'font': {'size': 30}}
    ))

    fig.update_layout(
        margin={'t': 0, 'b': 0, 'l': 0, 'r': 0},
        paper_bgcolor="lightgray",
        height=450
    )
    return fig

# --- UI Elements ---
name = st.text_input("Enter your name")

selected_mood = st.radio("How are you feeling today?", list(moods.keys()))

if selected_mood:
    mood_value = moods[selected_mood]
    fig = create_gauge(mood_value, selected_mood)
    st.plotly_chart(fig, use_container_width=True)

if st.button("Submit Mood"):
    if name.strip() == "":
        st.error("⚠️ Please enter your name before submitting.")
    else:
        df = pd.DataFrame({
            "Timestamp": [datetime.now()],
            "Name": [name.strip()],
            "Mood": [selected_mood]
        })

        if os.path.exists("mood_data.xlsx"):
            old_df = pd.read_excel("mood_data.xlsx")
            df = pd.concat([old_df, df], ignore_index=True)

        df.to_excel("mood_data.xlsx", index=False)
        st.success("✅ Mood submitted successfully!")
        st.balloons()
