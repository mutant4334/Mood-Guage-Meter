import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os

# Title
st.title("😃 Mood Survey")

# Mood options with Likert scale values
moods = {
    "Very Sad 😞": 1,
    "Sad 🙁": 2,
    "Neutral 😐": 3,
    "Happy 🙂": 4,
    "Very Happy 😃": 5
}

# Create a 3D-like gauge chart based on Likert scale
def create_gauge(selected_value, selected_mood_text):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=selected_value,
        number={
            'font': {'size': 40},
            'valueformat': '',
            'prefix': '',  
            'suffix': '',
            'font': {'color': 'black', 'size': 40},
            'text': selected_mood_text  # Set mood name in center
        },
        gauge={
            'axis': {
                'range': [1, 5],
                'tickvals': [1, 2, 3, 4, 5],
                'ticktext': ["Very Sad", "Sad", "Neutral", "Happy", "Very Happy"],
                'tickwidth': 2,
                'tickcolor': "darkblue"
            },
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

# Custom celebration animation
def celebrate_mood():
    st.success("🎉 Mood submitted successfully! 🎉")
    st.snow()  # prettier animation than balloons
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

# Display gauge only if mood is selected
if selected_mood:
    selected_value = moods[selected_mood]
    # Get mood text properly
    selected_mood_text = selected_mood.split(' ')[0]  # Extract first word like "Happy"
    st.plotly_chart(create_gauge(selected_value, selected_mood_text), use_container_width=True)

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
