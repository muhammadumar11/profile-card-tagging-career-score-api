# extract_score.py

import requests
import os

def generate_prompt(headline, position_summaries):
    prompt = f"Given the following:\nHeadline: {headline}\nPositions:\n"
    for pos in position_summaries:
        prompt += f"- {pos}\n"
    prompt += "\nOn a scale 0–100, rate this candidate’s career growth (rapid vs stagnant) and provide a one-sentence rationale. Format exactly as: <score> – <rationale>."
    return prompt

# def call_llm(prompt):
    hf_token = os.getenv("HF_TOKEN")
    hf_endpoint = os.getenv("HF_CAREER_EP")
    if not hf_token or not hf_endpoint:
        raise ValueError("HF_TOKEN and HF_CAREER_EP must be set as environment variables.")

    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt
    }
    response = requests.post(hf_endpoint, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()
    if isinstance(result, dict) and "generated_text" in result:
        return result["generated_text"]
    elif isinstance(result, list) and "generated_text" in result[0]:
        return result[0]["generated_text"]
    else:
        raise ValueError("Unexpected response format from HuggingFace model.")

def call_llm(prompt):
    # Stubbed return for assignment/demo
    return "75 – Rapid promotions in 2yr intervals."


def parse_llm_response(response_text):
    try:
        score_text, rationale = response_text.split("–", 1)
        score = int(score_text.strip())
        rationale = rationale.strip()
        return score, rationale
    except Exception as e:
        raise ValueError(f"Failed to parse LLM response: {e}")
