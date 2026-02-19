✅ Step 1 — Create AI Module

Create this file:

ai/description_generator.py


Add this code:

# ai/description_generator.py

import os
import requests

def generate_description(username, total_commits, top_language):
    """
    Generate an AI description of GitHub stats using HuggingFace Inference API.
    """

    api_token = os.getenv("HF_API_TOKEN")  # User must set this
    if not api_token:
        return "⚠️ HuggingFace API token not found. Please set HF_API_TOKEN."

    headers = {
        "Authorization": f"Bearer {api_token}"
    }

    prompt = f"""
    Generate a professional but creative summary of a GitHub user.

    Username: {username}
    Total Commits: {total_commits}
    Top Language: {top_language}

    Keep it short (3-4 lines).
    """

    payload = {
        "inputs": prompt
    }

    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/google/flan-t5-large",
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()
        result = response.json()

        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]

        return "AI could not generate description."

    except Exception as e:
        return f"Error generating description: {str(e)}"

✅ Step 2 — Update app.py

Add this import at the top:

from ai.description_generator import generate_description


Then add this inside the Streamlit UI section (after stats are calculated):

if st.button("Generate AI Description"):
    description = generate_description(
        username,
        total_commits,
        top_language
    )
    st.subheader("AI Generated Summary")
    st.write(description)

✅ Step 3 — Add to README.md

Add:

## AI Integration

This app now supports AI-generated descriptions of GitHub stats.

To enable:
1. Create a HuggingFace account
2. Generate an API token
3. Set environment variable:

export HF_API_TOKEN=your_token_here

4. Click "Generate AI Description" inside the app
