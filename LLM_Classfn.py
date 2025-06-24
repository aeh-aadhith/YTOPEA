import os
from groq import Groq
from keys import GROQ_API

client = Groq(api_key = GROQ_API)

def classify_title(title: str) -> str:
    """
    Classifies an ophthalmology video based on its title alone.
    """
    system_instruction = (
        "You are an expert classifier for ophthalmology content. "
        "Based only on a YouTube video title, return the best-matching category from: "
        "'surgical tutorial', 'new technology review', 'disease pathology', 'research update', 'patient interaction', 'conference highlight'. "
        "Return only the label, nothing else."
    )

    chat_completion = client.chat.completions.create(
        model="qwen-qwq-32b",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": title}
        ]
    )

    return chat_completion.choices[0].message.content.strip()

def classify_title_transcript(title: str, transcript: str) -> str:
    """
    Classifies an ophthalmology video based on its title and transcript.
    """
    system_instruction = (
        "You are an expert classifier for ophthalmology content. "
        "Based on the video title and transcript, return the most relevant category from: "
        "'surgical tutorial', 'new technology review', 'disease pathology', 'research update', 'patient interaction', 'conference highlight'. "
        "Return only the label, nothing else."
    )

    user_prompt = f"Title: {title}\nTranscript: {transcript}"

    chat_completion = client.chat.completions.create(
        model="qwen-qwq-32b",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ]
    )

    return chat_completion.choices[0].message.content.strip()

def classify_title_description(title: str, description: str) -> str:
    """
    Classifies an ophthalmology video based on its title and description.
    """
    system_instruction = (
        "You are an expert classifier for ophthalmology content. "
        "Based on the video title and description, return the most relevant category from: "
        "'surgical tutorial', 'new technology review', 'disease pathology', 'research update', "
        "'patient interaction', or 'conference highlight'. "
        "Return only the label, nothing else."
    )

    user_prompt = f"Title: {title}\nDescription: {description}"

    chat_completion = client.chat.completions.create(
        model="qwen-qwq-32b",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ]
    )

    return chat_completion.choices[0].message.content.strip()

def classify_title_description_transcript(title: str, description: str, transcript: str) -> str:
    """
    Classifies an ophthalmology video based on title, description, and transcript.
    """
    system_instruction = (
        "You are an expert classifier for ophthalmology content. "
        "Using the video title, description, and transcript, return the most relevant category from: "
        "'surgical tutorial', 'new technology review', 'disease pathology', 'research update', "
        "'patient interaction', or 'conference highlight'. "
        "Return only the label, nothing else."
    )

    user_prompt = f"Title: {title}\nDescription: {description}\nTranscript: {transcript}"

    chat_completion = client.chat.completions.create(
        model="qwen-qwq-32b",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ]
    )

    return chat_completion.choices[0].message.content.strip()

def extract_final_label(response: str) -> str:
    """
    Extracts the last non-empty line from a verbose LLM response.
    Final line contains the intended classification label.
    """
    lines = response.strip().splitlines()
    for line in reversed(lines):
        if line.strip():  # skip empty lines
            return line.strip()
    return "Unknown"

def classify_video(title=None, description=None, transcript=None):
    if not title:
        raise ValueError("Title is required for classification.")

    elif description and transcript:
        LLM_Response = classify_title_description_transcript(title, description, transcript)

    elif transcript:
        LLM_Response = classify_title_transcript(title, transcript)
    
    elif description:
        LLM_Response = classify_title_description(title, description)
    
    else:
        LLM_Response = classify_title(title)
    
    return extract_final_label(LLM_Response)


if __name__ == "__main__":
    label = classify_video(
        title="Managing glaucoma in rural India",
        description="This video outlines an outreach program...",
        transcript=None
    )
    print(label)