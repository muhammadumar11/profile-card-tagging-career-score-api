# app.py

from flask import Flask, request, jsonify
import pandas as pd
from extract_tags import compute_years_of_experience, compute_pharma_distribution
from extract_score import generate_prompt, call_llm, parse_llm_response

app = Flask(__name__)

# Load the data once at startup
profiles_df = pd.read_excel("profile_data.xlsx", sheet_name="profiles_rows")
positions_df = pd.read_excel("profile_data.xlsx", sheet_name="positions_rows")
educations_df = pd.read_excel("profile_data.xlsx", sheet_name="education_rows")

@app.route("/generate-profile", methods=["POST"])
def generate_profile():
    data = request.get_json()
    if not data or "profile_id" not in data:
        return jsonify({"error": "Missing profile_id"}), 400

    profile_id = data["profile_id"]
    profile = profiles_df[profiles_df["id"] == profile_id]

    if profile.empty:
        return jsonify({"error": "profile_id not found"}), 400

    full_name = profile.iloc[0]["full_name"]
    headline = profile.iloc[0]["headline"]

    user_positions = positions_df[positions_df["profile_id"] == profile_id]

    years_experience = compute_years_of_experience(user_positions)
    pharma_dist = compute_pharma_distribution(user_positions)

    position_summaries = user_positions.apply(
    lambda row: f"{row['title']} at {row['company_name']} - {str(row['description'])[:100]}", axis=1
    ).tolist()

    prompt = generate_prompt(headline, position_summaries)

    try:
        llm_response = call_llm(prompt)
        career_score, career_rationale = parse_llm_response(llm_response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    result = {
        "id": profile_id,
        "full_name": full_name,
        "years_of_experience": years_experience,
        "pharma_experience_distribution": pharma_dist,
        "career_progression_score": career_score,
        "career_rationale": career_rationale
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
