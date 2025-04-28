import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os

# Title
st.title("😃 Mood Survey)")

# Mood options with Likert scale values
moods = {
    "Very Sad 😞": 1,
    "Sad 🙁": 2,
    "Neutral 😐": 3,
    "Happy 🙂": 4,
    "Very Happy 😃": 5
}

# Create 3D-like gauge chart based on Likert scale
def create_gauge(selected_value, selected_mood_text):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=selected_value,
        number={'valueformat': '', 'font': {'size': 30}, 'prefix': f"{selected_mood_text} "},  # Show Mood Text instead of number
        gauge={
            'axis': {'range': [1, 5], 'tickvals': [1, 2, 3, 4, 5], 'ticktext': ["Very Sad", "Sad", "Neutral", "Happy", "Very Happy"], 'tickwidth': 2, 'tickcolor': "darkblue"},
            'borderwidth': 4,
            'bordercolor': "gray",
            'bar': {'color': "black", 'thickness': 0.2},
            'bgcolor': "white",
            'steps': [
                {'range': [1, 2], 'color': "#ff4b4b"},
                {'range': [2, 3], 'color': "#ffa500"},
                {'range': [3, 4], 'color': "#ffff00"},
                {'range': [4, 5], 'color': "#90ee90"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 6},
                'thickness': 0.8,
                'value': selected_value
            }
        },
        domain={'x': [0, 1], 'y': [0, 1]}
    ))

    fig.update_layout(
        paper_bgcolor="lightgray",
        font={'color': "black", 'family': "Arial"},
        margin=dict(l=50, r=50, t=50, b=50),
        width=600,
        height=400
    )
    return fig

# Input Name
name = st.text_input("Enter your name:", "")

# Mood selection
selected_mood = st.radio("How are you feeling today?", list(moods.keys()))

# Display gauge only if mood is selected
if selected_mood:
    selected_value = moods[selected_mood]
    selected_mood_text = selected_mood.split()[0]  # Only the mood word (e.g., "Happy", "Sad")
    st.plotly_chart(create_gauge(selected_value, selected_mood_text), use_container_width=True)

# Submit Button
if st.button("Submit Mood"):
    if name.strip() == "":
        st.error("Please enter your name before submitting.")
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

        st.success(f"Thank you {name.strip()}! Your mood '{selected_mood}' has been recorded! 🎯")
        st.balloons()  # 🎈 Little animation for success
