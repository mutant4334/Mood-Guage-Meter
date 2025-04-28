import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import os
from datetime import datetime

st.set_page_config(layout="wide")
st.title("😃 Mood Survey - Semi Circular Speedometer")

# Define moods with corresponding gauge values
moods = {
    "Very Sad": 10,
    "Sad": 30,
    "Neutral": 50,
    "Happy": 70,
    "Very Happy": 90
}

colors = ['#FF4B4B', '#FFA500', '#FFFF00', '#90EE90', '#32CD32']

# Function to create semi-circular speedometer
def create_semi_gauge(value, mood_label):
    # Create base pie chart for gauge background
    fig = go.Figure()

    fig.add_trace(go.Pie(
        values=[20, 20, 20, 20, 20, 100],  # 5 sections + hidden half
        rotation=180,
        hole=0.5,
        direction="clockwise",
        sort=False,
        marker_colors=colors + ["white"],
        textinfo='none'
    ))

    # Calculate the angle for the needle
    angle = (180 - (value / 100) * 180)

    # Needle
    fig.add_shape(type='line',
                  x0=0.5,
                  y0=0.5,
                  x1=0.5 + 0.4 * np.cos(np.radians(angle)),
                  y1=0.5 + 0.4 * np.sin(np.radians(angle)),
                  line=dict(color='black', width=4))

    # Update layout
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        height=400,
        paper_bgcolor="lightgray",
        annotations=[dict(text=f"<b>{mood_label}</b>", x=0.5, y=0.25, font_size=20, showarrow=False)]
    )

    return fig

# --- UI Elements ---
name = st.text_input("Enter your name")

selected_mood = st.radio("How are you feeling today?", list(moods.keys()))

if selected_mood:
    mood_value = moods[selected_mood]
    fig = create_semi_gauge(mood_value, selected_mood)
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
