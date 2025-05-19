import streamlit as st
import pandas as pd
import os

def load_course_fit_results():
    file_path = os.path.join("data", "processed", "charles_schwab_top5.csv")
    if not os.path.exists(file_path):
        return "The course fit model hasn't been run yet. Please run course_fit.py first."

    df = pd.read_csv(file_path)
    top_players = df[['player_name', 'fit_score']].head(10)

    message = "\n🏌️‍♂️ Top Players Based on Course Fit at Colonial:\n\n"
    for idx, row in top_players.iterrows():
        message += f"{idx + 1}. {row['player_name']} — Fit Score: {row['fit_score']:.2f}\n"
    return message

st.set_page_config(page_title="PGA Course Fit Chatbot", layout="centered")
st.title("🏌️‍♂️ PGA Course Fit Chatbot")
st.markdown("Ask me about this week's best-fit players!")

query = st.text_input("Your question:")

if query:
    if any(k in query.lower() for k in ["colonial", "charles schwab", "fit", "top players"]):
        response = load_course_fit_results()
    else:
        response = "Try asking about the best players for Colonial or this week's tournament."
    st.text_area("Bot Response:", value=response, height=300, max_chars=None, key=None)
