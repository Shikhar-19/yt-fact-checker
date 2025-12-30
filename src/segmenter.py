import os
import json
import glob
import subprocess
import spacy

CAPTION_DIR = "yt_captions"
os.makedirs(CAPTION_DIR, exist_ok=True)

# --- Load SpaCy NLP model ---
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


# --------------------------------------------
# Helper → Extract video ID from various inputs
# --------------------------------------------
def extract_video_id(value: str):
    """
    Accepts:
      - direct YouTube ID
      - full YouTube URL
      - youtu.be link
      - local file path
    Returns:
      - ("youtube", video_id)
      - ("local", file_path)
    """

    # Case 1: Local transcript file
    if os.path.exists(value):
        return ("local", value)

    # Case 2: Full YouTube URL formats
    if "youtube.com/watch?v=" in value:
        return ("youtube", value.split("watch?v=")[1][:11])

    if "youtu.be/" in value:
        return ("youtube", value.split("youtu.be/")[1][:11])

    # Case 3: Assume raw YouTube ID (length 11)
    if len(value) == 11:
        return ("youtube", value)

    # Unknown format
    return ("unknown", value)


# -------------------------------------------------------
# Load local JSON3 or text transcript & split into sentences
# -------------------------------------------------------
def load_local_transcript(path: str):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            data = f.read()

        # If it's JSON3
        if path.endswith(".json3"):
            try:
                json_data = json.loads(data)
                lines = []

                for event in json_data.get("events", []):
                    if "segs" in event:
                        for seg in event["segs"]:
                            t = seg.get("utf8", "").strip().replace("\n", " ")
                            lines.append(t)

                text = " ".join(lines)
            except:
                text = data  # fallback: treat as raw text

        else:
            text = data

        # Split into sentences
        doc = nlp(text)
        return [sent.text.strip() for sent in doc.sents]

    except Exception as e:
        print("Error reading local transcript:", e)
        return []


# -------------------------------------------------------
# Download transcript with yt-dlp and extract sentences
# -------------------------------------------------------
def load_youtube_transcript(video_id: str):
    url = f"https://www.youtube.com/watch?v={video_id}"
    output_template = os.path.join(CAPTION_DIR, f"{video_id}.%(ext)s")

    try:
        subprocess.run(
            [
                "yt-dlp",
                "--skip-download",
                "--write-auto-subs",
                "--sub-lang", "en",
                "--sub-format", "json3",
                "-o", output_template,
                url
            ],
            capture_output=True,
            text=True
        )

        caption_files = glob.glob(f"{CAPTION_DIR}/{video_id}*.json3")
        if not caption_files:
            print("❌ No subtitle file found.")
            return []

        with open(caption_files[0], "r", encoding="utf-8") as f:
            data = json.load(f)

        lines = []
        for event in data.get("events", []):
            if "segs" in event:
                for seg in event["segs"]:
                    t = seg.get("utf8", "").strip().replace("\n", " ")
                    lines.append(t)

        text = " ".join(lines)

        doc = nlp(text)
        return [sent.text.strip() for sent in doc.sents]

    except Exception as e:
        print("❌ Unexpected error:", e)
        return []


# -------------------------------------------------------
# MAIN ENTRY — Unified interface
# -------------------------------------------------------
def get_video_sentences(input_value: str):
    mode, data = extract_video_id(input_value)

    if mode == "local":
        print(f"📄 Using local transcript: {data}")
        return load_local_transcript(data)

    if mode == "youtube":
        print(f"📺 Fetching YouTube transcript for video ID: {data}")
        return load_youtube_transcript(data)

    print("❌ Unsupported input format:", input_value)
    return []


# Standalone test
if __name__ == "__main__":
    # You can test using:
    # 1. YouTube ID: "Ks-_Mh1QhMc"
    # 2. YouTube URL: "https://youtu.be/Ks-_Mh1QhMc"
    # 3. Local file: "yt_captions/Ks-_Mh1QhMc.en.json3"
    test_input = "Ks-_Mh1QhMc"

    sentences = get_video_sentences(test_input)
    print("Extracted:", len(sentences))
    print("First 5:", sentences[:5])
