import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import os
from datetime import datetime

st.set_page_config(layout="wide")
st.title("😃 Mood Survey - Speedometer Style")

# Mood options with values
moods = {
    "Very Sad 😞": 10,
    "Sad 🙁": 30,
    "Neutral 😐": 50,
    "Happy 🙂": 70,
    "Very Happy 😃": 90
}

# Create the gauge chart
def create_speedometer(value, label):
    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        gauge={
            'shape': "semi",
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "black", 'thickness': 0.3},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 20], 'color': '#FF4B4B'},
                {'range': [20, 40], 'color': '#FFA500'},
                {'range': [40, 60], 'color': '#FFFF00'},
                {'range': [60, 80], 'color': '#90EE90'},
                {'range': [80, 100], 'color': '#32CD32'}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 6},
                'thickness': 0.8,
                'value': value
            }
        },
        title={'text': label, 'font': {'size': 24}}
    ))

    fig.update_layout(
        margin={'t': 0, 'b': 0, 'l': 0, 'r': 0},
        paper_bgcolor="white",
        height=400
    )

    return fig

# Input fields
name = st.text_input("Enter your name:")

selected_mood = st.radio("How are you feeling today?", list(moods.keys()))

if selected_mood:
    mood_value = moods[selected_mood]
    mood_label = selected_mood.split()[0]
    fig = create_speedometer(mood_value, mood_label)
    st.plotly_chart(fig, use_container_width=True)

if st.button("Submit Mood"):
    if name.strip() == "":
        st.error("⚠️ Please enter your name before submitting.")
    else:
        # Save to Excel
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

        # Success animation
        st.success("🎉 Mood submitted successfully! 🎉")
        st.balloons()
