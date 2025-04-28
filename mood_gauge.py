# mood_gauge_with_animation.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- Mood Settings ---

mood_emojis = ["😡", "😞", "😐", "😊", "🤩"]  # Emojis for the moods
mood_labels = ["Angry", "Sad", "Neutral", "Happy", "Excited"]  # Text labels (hidden)
mood_angles = [0, 45, 90, 135, 180]  # Degrees on semi-circle

mood_to_angle = dict(zip(mood_labels, mood_angles))

# --- Initialize Session Storage ---

if 'responses' not in st.session_state:
    st.session_state.responses = []

# --- Streamlit App UI ---

st.set_page_config(page_title="Mood Gauge Survey", page_icon="😊", layout="centered")

st.title("🌈 Mood Survey (with Speedometer!)")
st.write("Tell us how you're feeling today!")

# Input Form
with st.form("mood_form", clear_on_submit=True):
    name = st.text_input("Your Name (optional)")
    selected_mood = st.radio("Select your Mood:", mood_labels, index=2)  # Default Neutral
    comment = st.text_area("Any Comments?")
    submit = st.form_submit_button("Submit")

# --- Handle Submission ---

if submit:
    new_response = {
        'Name': name,
        'Mood': selected_mood,
        'Comment': comment,
        'Timestamp': pd.Timestamp.now()
    }
    st.session_state.responses.append(new_response)
    st.success("✅ Thank you! Your response has been recorded.")

# --- Show Mood Gauge (Speedometer) with Emojis ---

if st.session_state.responses:
    latest_mood = st.session_state.responses[-1]['Mood']
    angle = mood_to_angle[latest_mood]

    # Create figure
    fig = go.Figure()

    # Add semicircular gauge with emojis
    fig.add_trace(go.Pie(
        values=[20, 20, 20, 20, 20, 100],
        rotation=90,
        hole=0.5,
        marker_colors=['red', 'orange', 'gray', 'lightgreen', 'green', 'white'],
        text=mood_emojis + [''],  # Emojis here
        textinfo='label',
        hoverinfo='none',
        direction='clockwise',
        sort=False,
        showlegend=False
    ))

    # Add Arrow Needle (using an annotation)
    fig.add_layout_image(
        dict(
            source="https://upload.wikimedia.org/wikipedia/commons/3/3e/Arrow_right.svg",  # Simple arrow image
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            sizex=0.5, sizey=0.5,
            xanchor="center",
            yanchor="middle",
            layer="above"
        )
    )

    # Define animation frames
    frames = []
    for i in range(5):  # One for each mood
        angle_frame = mood_to_angle[mood_labels[i]]
        frames.append(go.layout.Frame(
            data=[go.Scatter(
                x=[0.5 + 0.4 * pd.np.cos(pd.np.deg2rad(180 - angle_frame))],
                y=[0.5 + 0.4 * pd.np.sin(pd.np.deg2rad(180 - angle_frame))],
                mode='markers+text',
                marker=dict(symbol="arrow-bar-up", size=15, angleref="paper"),
            )],
            name=f"Frame_{i}",
        ))

    # Add frames and layout
    fig.frames = frames
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor="white",
        updatemenus=[
            {
                'buttons': [
                    {
                        'args': [None, {'frame': {'duration': 1000, 'redraw': True}, 'fromcurrent': True}],
                        'label': 'Play',
                        'method': 'animate'
                    },
                    {
                        'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate'}],
                        'label': 'Pause',
                        'method': 'animate'
                    }
                ],
                'direction': 'left',
                'pad': {'r': 10, 't': 87},
                'showactive': False,
                'type': 'buttons',
                'x': 0.1,
                'xanchor': 'right',
                'y': 0,
                'yanchor': 'top',
            }
        ]
    )

    st.plotly_chart(fig, use_container_width=True)

# --- Download all responses ---

if st.session_state.responses:
    st.subheader("📋 All Responses")
    df = pd.DataFrame(st.session_state.responses)
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False)
    st.download_button(
        label="⬇️ Download Responses as CSV",
        data=csv,
        file_name="mood_survey_responses.csv",
        mime="text/csv"
    )
