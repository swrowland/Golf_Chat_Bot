import pandas as pd
import numpy as np
import os
from datetime import datetime

# Load clustered player data
data_path = os.path.join("data", "processed", "clustered_players.csv")
df = pd.read_csv(data_path)

# Load course historical scoring data
course_scores_path = os.path.join("data", "course_profiles", "colonial_scoring.csv")
if os.path.exists(course_scores_path):
    course_scores = pd.read_csv(course_scores_path)
    df = df.merge(course_scores, on='player_name', how='left')
    df['historical_colonial'] = df['historical_colonial'].fillna(0)
else:
    df['historical_colonial'] = 0
    print("Warning: Colonial historical course scoring file not found. Skipping this factor.")

# Load recent form data
recent_form_path = os.path.join("data", "processed", "recent_form.csv")
if os.path.exists(recent_form_path):
    recent_form = pd.read_csv(recent_form_path)
    df = df.merge(recent_form, on='player_name', how='left')
    df['recent_form'] = df['recent_form'].fillna(0)
else:
    df['recent_form'] = 0
    print("Warning: Recent form file not found. Skipping this factor.")

# === DEFAULT COURSE PROFILE FOR COLONIAL ===
course_profile = {
    "sg_ott": 0.3,
    "driving_accuracy": 1.0,
    "sg_app": 1.0,
    "sg_arg": 0.5,
    "sg_putt": 1.0,
    "historical_colonial": 0.8,
    "recent_form": 0.7
}

# Allow user to override the course profile
user_override = input("Would you like to adjust the course weights? (y/n): ")
if user_override.lower() == 'y':
    for key in course_profile:
        try:
            val = float(input(f"Enter weight for {key} (default={course_profile[key]}): "))
            course_profile[key] = val
        except ValueError:
            print(f"Keeping default weight for {key}.")

# Calculate player fit score based on weighted profile
def score_player(row, profile):
    score = 0
    for stat, weight in profile.items():
        if stat in row:
            score += row[stat] * weight
    return score

df['fit_score'] = df.apply(score_player, profile=course_profile, axis=1)
df_sorted = df.sort_values(by='fit_score', ascending=False)

top5 = df_sorted[['player_name', 'fit_score']].head(5)

print("\nTop 5 Players for This Week Based on Course Fit:")
print(top5.to_string(index=False))

# Save results
output_dir = os.path.join("data", "processed")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "charles_schwab_top5.csv")
df_sorted.to_csv(output_path, index=False)
print(f"\nFull ranked player list saved to {output_path}")
