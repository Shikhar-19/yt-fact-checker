# src/pipeline.py

import json

from src.segmenter import get_video_sentences
from src.model_loader import load_claim_classifier
from src.triage import classify_sentences
from src.fact_checker import verify_claim


def run_pipeline(video_id: str):
    print(f"\n=== FACT CHECKING VIDEO: {video_id} ===\n")

    # -----------------------------
    # 1. Load the classifier model
    # -----------------------------
    classifier = load_claim_classifier()

    # -----------------------------
    # 2. Extract transcript sentences
    # -----------------------------
    sentences = get_video_sentences(video_id)
    print(f"Extracted {len(sentences)} sentences")

    # -----------------------------
    # 3. Classify each sentence
    # -----------------------------
    triage_result = classify_sentences(sentences, classifier)

    trusted = triage_result["trusted"]      # factual claims
    disputed = triage_result["disputed"]    # disputed claims
    ignored = triage_result["ignored"]      # not claims

    print(f"\nTrusted: {len(trusted)} | Disputed: {len(disputed)} | Ignored: {ignored}\n")

    # -----------------------------
    # 4. Fact-check ALL factual claims
    # -----------------------------
    factual_checked = []
    for item in trusted:
        sent = item["sentence"]
        score = item["score"]

        print(f"Checking factual claim:\n→ {sent}\n")

        llm_verdict = verify_claim(sent)

        factual_checked.append({
            "sentence": sent,
            "model_score": score,
            "fact_check": llm_verdict
        })

    # -----------------------------
    # 5. Fact-check disputed claims
    # -----------------------------
    disputed_checked = []
    for item in disputed:
        sent = item["sentence"]
        score = item["score"]

        print(f"Checking disputed claim:\n→ {sent}\n")

        llm_verdict = verify_claim(sent)

        disputed_checked.append({
            "sentence": sent,
            "model_score": score,
            "fact_check": llm_verdict
        })

    # -----------------------------
    # 6. Build final structured JSON
    # -----------------------------
    report = {
        "video_id": video_id,
        "total_sentences": len(sentences),

        "counts": {
            "factual_claims": len(trusted),
            "disputed_claims": len(disputed),
            "ignored": ignored
        },

        "factual_claims_verified": factual_checked,
        "disputed_claims_verified": disputed_checked,
    }

    return report


# Standalone test
if __name__ == "__main__":
    test_id = "Ks-_Mh1QhMc"
    result = run_pipeline(test_id)

    print("\n=== FINAL REPORT ===")
    print(json.dumps(result, indent=4))
