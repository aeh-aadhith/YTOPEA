# 📻 YTOPEA: YouTube Ophthalmology Education & Pattern Analysis

YTOPEA is a Python-based tool that:

- Extracts video metadata from YouTube channels run by ophthalmologists or eye hospitals
- Retrieves transcripts (if available)
- Classifies videos into categories like surgical tutorials, research updates, or new technology reviews
- Helps analyze trends in online ophthalmology education

---

## 🚀 Features

- 📅 Pulls videos and metadata from any public YouTube channel
- 🧠 Uses LLM (Groq API + Qwen 32B) to classify videos
- 🎯 Supports classification via title, description, and transcript (when available)
- 🧼 Clean modular code structure for easy extension and reuse

---

## 📦 Setup Instructions

1. Clone the repo:

```bash
git clone https://github.com/aeh-aadhith/YTOPEA.git
cd YTOPEA
```

2. Install required libraries:

```bash
pip install -r requirements.txt
```

3. Add your API keys in a keys.py file:

```python
# keys.py
GROQ_API = "your-groq-api-key"
YOUTUBE_API = "your-youtube-api-key"
```

(Important: This file is in .gitignore and won't be committed)

---

## ▶️ How to Use

Run the main script to extract and classify videos from one or more YouTube channels:

```bash
python main.py
```

Output: A CSV file (e.g., classified\_videos.csv) with titles, metadata, and predicted category.

---

## 🧠 Classification Categories

The model classifies each video into one of the following:

- surgical tutorial
- new technology review
- disease pathology
- research update
- patient interaction
- conference highlight

---

## 📂 Project Structure

```
YTOPEA/
├── main.py                     # Main runner
├── get_transcript.py          # YouTube transcript fetching
├── video_data_extraction.py   # Channel + video metadata tools
├── LLM_Classfn.py             # LLM classification logic
├── tools.py                   # Utility functions (if any)
├── .gitignore
├── requirements.txt
├── keys.py
└── README.md
```

---

## 📄 License

MIT License (add LICENSE file if needed)

---

## 🙇‍♂️ Author

**Aadhith Manoj**\
Created at CODA, Aravind Eye Hospital Chennai

