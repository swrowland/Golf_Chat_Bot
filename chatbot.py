import pandas as pd
import os

def load_course_fit_results():
    file_path = os.path.join("data", "processed", "charles_schwab_top5.csv")
    if not os.path.exists(file_path):
        return "The course fit model hasn't been run yet. Please run course_fit.py first."

    df = pd.read_csv(file_path)
    top_players = df[['player_name', 'fit_score']].head(10)

    message = "Here are the top players based on course fit for Colonial (including historical data and recent form):\n"
    for idx, row in top_players.iterrows():
        message += f"{idx + 1}. {row['player_name']} — Fit Score: {row['fit_score']:.2f}\n"
    return message

def handle_user_query(query):
    query = query.lower()
    if "colonial" in query or "charles schwab" in query or "course fit" in query:
        return load_course_fit_results()
    return "Sorry, I didn't understand that. Try asking about player fits for Colonial or this week's tournament."

if __name__ == "__main__":
    print("Welcome to the Golf AI Chatbot! Type your question below.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = handle_user_query(user_input)
        print("Bot:", response)
