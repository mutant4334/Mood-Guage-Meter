import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os

# Title
st.title("😃 Mood Survey - Likert Scale (with Custom Gauge)")

# Mood options with Likert scale values
moods = {
    "Very Sad 😞": 1,
    "Sad 🙁": 2,
    "Neutral 😐": 3,
    "Happy 🙂": 4,
    "Very Happy 😃": 5
}

colors = ["#ff4b4b", "#ffa500", "#ffff00", "#90ee90", "#32CD32"]  # 5 color blocks

# Create custom semi-circle gauge
def create_custom_gauge(mood_text, mood_index):
    fig = go.Figure()

    fig.add_trace(go.Pie(
        values=[20]*5 + [100],
        marker_colors=colors + ["lightgray"],
        hole=0.5,
        direction="clockwise",
        sort=False,
        rotation=180,
        text=["Very Sad", "Sad", "Neutral", "Happy", "Very Happy", ""],
        textinfo="none",  # No small texts on blocks
        hoverinfo="skip",
        showlegend=False
    ))

    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        width=600,
        height=400,
        paper_bgcolor="lightgray",
        annotations=[dict(
            text=f"<b>{mood_text}</b>",
            x=0.5, y=0.3,
            font_size=30,
            showarrow=False
        )]
    )
    return fig

# Celebration animation
def celebrate_mood():
    st.success("🎉 Mood submitted successfully! 🎉")
    st.snow()
    st.markdown(
        """
        <div style='text-align: center; font-size:30px; color:green;'>
            🎊 Thank you for sharing your mood! 🎊
        </div>
        """, unsafe_allow_html=True
    )

# Input Name
name = st.text_input("Enter your name:", "")

# Mood selection
selected_mood = st.radio("How are you feeling today?", list(moods.keys()))

# Display custom gauge only if mood is selected
if selected_mood:
    mood_index = moods[selected_mood]
    mood_label = selected_mood.split(' ')[0]  # Only the mood word (Very, Sad, etc.)
    emoji = selected_mood.split(' ')[-1]      # Extract emoji separately

    # Proper Mood Name for Center (ignore "Very" if any)
    if mood_label == "Very":
        mood_label = selected_mood.split(' ')[1]

    st.plotly_chart(create_custom_gauge(mood_label, mood_index), use_container_width=True)

# Submit Button
if st.button("Submit Mood"):
    if name.strip() == "":
        st.error("⚠️ Please enter your name before submitting.")
    else:
        # Save response
        data = {
            "Timestamp": [datetime.now()],
            "Name": [name.strip()],
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

        celebrate_mood()
