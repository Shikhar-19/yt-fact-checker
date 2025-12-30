# 🧠 YouTube Fact Checker (AI-Powered)

An end-to-end **AI Fact-Checking System** that:

- Downloads & extracts YouTube transcripts
- Splits the transcript into sentences (spaCy)
- Classifies each sentence using a **custom RoBERTa claim-classifier**
- Fact-checks all claims using **LLaMA 3 (via Ollama)**
- Generates a **detailed HTML / PDF report**
- Provides a **FastAPI backend** + **Streamlit UI**

👉 Ideal for research, misinformation analysis, YouTube content analysis, and academic demos.

---

## 🚀 Features

### ✅ 1. Transcript Extraction

- Supports **YouTube URLs**, **YouTube IDs**, and **local transcript files (`.json3`)**
- Uses `yt-dlp` for auto-subtitle extraction

### ✅ 2. Sentence Segmentation

- Uses **spaCy** (`en_core_web_sm`) to split transcript into clean sentences

### ✅ 3. Claim Classification

Uses a **fine-tuned RoBERTa model** to classify sentences into:

- `FACTUAL_CLAIM`
- `DISPUTED_CLAIM`
- `NOT_A_CLAIM`

### ✅ 4. LLM Fact Verification

For each claim, the system checks truthfulness using:

- **LLaMA 3.1 8B via Ollama**

Provides structured JSON:

```json
{
  "verdict": "TRUE / FALSE / PARTIALLY TRUE / UNVERIFIABLE",
  "explanation": "Short reasoning",
  "evidence": []
}
```

### ✅ 5. Output Report

Generates:

- HTML Report
- (Optional) PDF Report via wkhtmltopdf

✅ 6. UI + API

- FastAPI backend for pipeline execution

- Streamlit UI for simple user-friendly interface

## 📂 Project Structure

```
youtube-fact-checker/
│
├── model/ # NOT included in repo (download separately)
│
├── reports/ # (auto-created) saved HTML / PDF results
│
├── src/
│ ├── app.py # FastAPI backend
│ ├── streamlit_app.py # Streamlit UI
│ ├── pipeline.py # Main logic orchestrator
│ ├── model_loader.py # Loads RoBERTa classifier
│ ├── fact_checker.py # Calls LLaMA (Ollama)
│ ├── segmenter.py # Transcript extraction + spaCy split
│ ├── triage.py # Claim classification
│ ├── report_generator.py
│ └── evaluate_classifier.py # test robustness of classifier
│
├── yt_captions/ # Auto-downloaded captions
│
├── requirements.txt
├── .gitignore
└── README.md
```

## 📥 Model Download (IMPORTANT)

The trained RoBERTa model is too large for GitHub.

📌 Download the model folder from Google Drive:
👉 [Link](https://drive.google.com/file/d/1tTpVDudmCzzR7kyBYxouhDYCb1_6xu8x/view?usp=sharing)

After downloading:

```
youtube-fact-checker/
│
└── model/
      ├── config.json
      ├── merges.txt
      ├── model.safetensors
      ├── special_tokens_map.json
      ├── tokenizer.json
      ├── tokenizer_config.json
      ├── training_args.bin
      ├── vocab.json
```

## ⚙️ Installation (No venv required)

Anyone cloning the repo can run this project by following these steps:

### 1️⃣ Install Python 3.10+

Download from: https://www.python.org/downloads/

### 2️⃣ Install Requirements

Open terminal inside project folder:

```bash
pip install -r requirements.txt
```

### 3️⃣ Install Ollama

Download & install:
👉 https://ollama.com/download

Then pull the model:

```bash
ollama pull llama3.1:8b
```

### 4️⃣ (Optional) Install PDF Export Support

Install wkhtmltopdf (required):
👉 https://wkhtmltopdf.org/downloads.html

Run in terminal inside project folder

```bash
pip install pdfkit
```

## ▶️ Run the Project

### Start the FastAPI Backend

```bash
uvicorn src.app:app --reload
```

### Start Streamlit UI

(Run in another terminal)

```bash
streamlit run src/streamlit_app.py
```

## 🎯 Usage

Paste a YouTube URL in Streamlit:

```bash
https://www.youtube.com/watch?v=XXXXXXX
```

## 🧾 SAMPLE OUTPUT

### A sample result looks like:

```
Total sentences: 98
Factual claims: 12
Disputed claims: 4
Ignored: 82
```

### Example factual claim:

```
Sentence: "Water boils at 100°C at sea level."
Model Score: 0.97
Verdict: TRUE
Explanation: Scientific fact confirmed.
Evidence:
- Source: Wikipedia
  Description: Water boiling point at 1 atm is 100°C.
```

### Example disputed claim:

```
Sentence: "The earth is flat."
Model Score: 0.99
Verdict: FALSE
Explanation: Overwhelming scientific evidence contradicts this.
Evidence:
- Source: NASA
  Description: Earth is an oblate spheroid.
```

![Demo Screenshot](https://github.com/AyushRawat1718/youtube-fact-checker/blob/main/Screenshot/Screenshot1718.png)

## 🧩 Tech Stack

```
| Component             | Technology            |
| --------------------- | --------------------- |
| Transcript Extraction | yt-dlp                |
| Sentence Splitting    | spaCy                 |
| Claim Classification  | Custom RoBERTa model  |
| Fact Checking         | LLaMA 3.1 8B (Ollama) |
| Backend               | FastAPI               |
| Frontend              | Streamlit             |
| Report Generation     | HTML / PDF            |
```

## ✨ Credits

- Built with passion by `Shikhar Gupta` ✨
  This project was inspired by modern misinformation-detection research and designed for clarity, usability, and real-world utility.

- If this tool helps you, consider giving the repo a ⭐ on GitHub!

## 🤝 Contributing

Contributions are warmly welcomed!
Whether it's improving accuracy, extending the UI, or optimizing the pipeline — your help makes this project better

1. Fork the repository
2. Create a new branch (feature/new-feature)
3. Commit your changes
4. Open a pull request 🚀
