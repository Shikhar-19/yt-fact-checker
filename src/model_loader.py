from transformers import pipeline
import os

MODEL_PATH = "./model"

class ClaimClassifier:
    def __init__(self, model_path=MODEL_PATH):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model folder not found at {model_path}")
        
        print(f"Loading model from {model_path}...")

        self.model = pipeline(
            "text-classification",
            model=model_path,
            tokenizer=model_path,
            device=-1   # CPU, change to 0 for GPU
        )

        print("Model loaded successfully.")

    def predict(self, sentence: str):
        result = self.model(sentence)[0]
        
        raw_label = result["label"]        # e.g. "LABEL_1"
        score = result["score"]
        
        # Convert LABEL_X → X
        if raw_label.startswith("LABEL_"):
            label_id = int(raw_label.split("_")[1])
        else:
            label_id = raw_label

        return label_id, score

def load_claim_classifier():
    return ClaimClassifier()
        

if __name__ == "__main__":
    clf = ClaimClassifier()
    tests = [
        "The moon landing was faked.",
        "Water boils at 100 degrees Celsius.",
        "I love this video."
    ]
    for t in tests:
        print(t, "=>", clf.predict(t))
