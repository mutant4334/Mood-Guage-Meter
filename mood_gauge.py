import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import os
from datetime import datetime

st.set_page_config(layout="wide")
st.title("😃 Mood Survey - Full Circular Speedometer with Mood Labels")

# Define moods with corresponding gauge angles and colors
moods = {
    "Very Sad 😞": (10, "#FF4B4B"),
    "Sad 🙁": (30, "#FFA500"),
    "Neutral 😐": (50, "#FFFF00"),
    "Happy 🙂": (70, "#90EE90"),
    "Very Happy 😃": (90, "#32CD32")
}

# Function to create full circular gauge
def create_full_gauge(value, mood_label, full_mood_name):
    fig = go.Figure()

    # Add pie slices with mood labels inside
    fig.add_trace(go.Pie(
        values=[20]*5,  # Equal sections
        hole=0.5,
        direction="clockwise",
        sort=False,
        marker_colors=[moods[m][1] for m in moods],
        text=[m for m in moods.keys()],
        textinfo='text',
        textposition='inside',
        insidetextorientation='radial',
        font=dict(size=14, color="black")
    ))

    # Calculate needle angle
    angle = (value / 100) * 360

    # Needle shaft
    fig.add_shape(
        type='line',
        x0=0.5,
        y0=0.5,
        x1=0.5 + 0.35 * np.cos(np.radians(angle - 90)),
        y1=0.5 + 0.35 * np.sin(np.radians(angle - 90)),
        line=dict(color='black', width=6)
    )

    # Arrowhead triangle
    fig.add_shape(
        type="path",
        path=f'M {0.5 + 0.35 * np.cos(np.radians(angle - 90))} {0.5 + 0.35 * np.sin(np.radians(angle - 90))} '
             f'L {0.5 + 0.32 * np.cos(np.radians(angle - 90) + 0.1)} {0.5 + 0.32 * np.sin(np.radians(angle - 90) + 0.1)} '
             f'L {0.5 + 0.32 * np.cos(np.radians(angle - 90) - 0.1)} {0.5 + 0.32 * np.sin(np.radians(angle - 90) - 0.1)} Z',
        fillcolor="black",
        line_color="black"
    )

    # Center circle
    fig.add_shape(
        type="circle",
        x0=0.48, y0=0.48,
        x1=0.52, y1=0.52,
        fillcolor="black",
        line_color="black"
    )

    # Update layout
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        height=550,
        paper_bgcolor="lightgray",
        annotations=[dict(text=f"<b>{full_mood_name}</b>", x=0.5, y=0.5, font_size=20, showarrow=False)]
    )

    return fig

# --- UI Elements ---
name = st.text_input("Enter your name")

if name.strip() != "":
    selected_mood = st.radio("How are you feeling today?", list(moods.keys()))
    
    if selected_mood:
        mood_value, mood_color = moods[selected_mood]
        fig = create_full_gauge(mood_value, selected_mood.split()[0], selected_mood)
        st.plotly_chart(fig, use_container_width=True)

    if st.button("Submit Mood"):
        df = pd.DataFrame({
            "Timestamp": [datetime.now()],
            "Name": [name.strip()],
            "Mood": [selected_mood],
            "Emoji": [selected_mood.split()[-1]]
        })

        if os.path.exists("mood_data.xlsx"):
            old_df = pd.read_excel("mood_data.xlsx")
            df = pd.concat([old_df, df], ignore_index=True)

        df.to_excel("mood_data.xlsx", index=False)
        st.success("✅ Mood submitted successfully!")
        st.balloons()

else:
    st.warning("⚠️ Please enter your name first to select mood.")
