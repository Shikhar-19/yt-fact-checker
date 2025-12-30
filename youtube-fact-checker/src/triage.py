# triage.py

def classify_sentences(sentences, classifier):
    """
    Classifies sentences using string labels the classifier returns:
        'FACTUAL_CLAIM'
        'DISPUTED_CLAIM'
        'NOT_A_CLAIM'
    """

    trusted = []
    disputed = []
    ignored = 0

    for sent in sentences:
        label, score = classifier.predict(sent)

        # Case 1: Factual
        if label == "FACTUAL_CLAIM":
            trusted.append({
                "sentence": sent,
                "score": score
            })

        # Case 2: Disputed
        elif label == "DISPUTED_CLAIM":
            disputed.append({
                "sentence": sent,
                "score": score
            })

        # Case 3: Not a claim
        else:
            ignored += 1

    return {
        "trusted": trusted,
        "disputed": disputed,
        "ignored": ignored
    }


# Standalone test
if __name__ == "__main__":
    from model_loader import ClaimClassifier
    from segmenter import get_video_sentences

    video_id = "Ks-_Mh1QhMc"
    sentences = get_video_sentences(video_id)

    classifier = ClaimClassifier()
    results = classify_sentences(sentences, classifier)

    print("Trusted:", len(results["trusted"]))
    print("Disputed:", len(results["disputed"]))
    print("Ignored:", results["ignored"])
