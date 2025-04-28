import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os

# Title
st.title("😃 Mood Survey")

# Mood options
moods = {
    "Very Sad 😞": 0,
    "Sad 🙁": 45,
    "Neutral 😐": 90,
    "Happy 🙂": 135,
    "Very Happy 😃": 180
}

# Create gauge chart
def create_gauge(selected_angle):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=selected_angle,
        gauge={
            'axis': {'range': [0, 180]},
            'steps': [
                {'range': [0, 36], 'color': "#ff4b4b"},
                {'range': [36, 72], 'color': "#ffa500"},
                {'range': [72, 108], 'color': "#ffff00"},
                {'range': [108, 144], 'color': "#90ee90"},
                {'range': [144, 180], 'color': "#008000"}
            ],
            'bar': {'color': "black", 'thickness': 0.3}
        }
    ))
    fig.update_layout(width=600, height=400)
    return fig

# Select Mood
selected_mood = st.radio("How are you feeling today?", list(moods.keys()))

if selected_mood:
    # Show animated gauge
    st.plotly_chart(create_gauge(moods[selected_mood]), use_container_width=True)

    # Submit Button
    if st.button("Submit Mood"):
        # Save response
        data = {
            "Timestamp": [datetime.now()],
            "Mood": [selected_mood],
            "Emoji": [selected_mood.split()[-1]]
        }
        df = pd.DataFrame(data)
        
        # If file exists, append, else create
        if os.path.exists("mood_responses.xlsx"):
            existing_df = pd.read_excel("mood_responses.xlsx")
            final_df = pd.concat([existing_df, df], ignore_index=True)
        else:
            final_df = df

        final_df.to_excel("mood_responses.xlsx", index=False)
        
        st.success(f"Your mood '{selected_mood}' has been recorded! 🎯")
