# src/evaluate_classifier.py

from model_loader import load_claim_classifier
import json

# ------------------------------
# 40 Benchmark Test Sentences
# ------------------------------

TEST_DATA = [
    ("Water boils at 100 degrees Celsius at sea level.", "FACTUAL_CLAIM"),
    ("The human body has 206 bones.", "FACTUAL_CLAIM"),
    ("Mount Everest is the tallest mountain on Earth above sea level.", "FACTUAL_CLAIM"),
    ("The Pacific Ocean is the largest ocean on Earth.", "FACTUAL_CLAIM"),
    ("Light travels at approximately 300,000 kilometers per second.", "FACTUAL_CLAIM"),
    ("The capital of France is Paris.", "FACTUAL_CLAIM"),
    ("Bananas contain potassium.", "FACTUAL_CLAIM"),
    ("The Earth revolves around the Sun.", "FACTUAL_CLAIM"),
    ("Brazil is the largest country in South America.", "FACTUAL_CLAIM"),
    ("Sharks have existed longer than trees.", "FACTUAL_CLAIM"),

    ("Vaccines contain microchips.", "DISPUTED_CLAIM"),
    ("The Earth is flat.", "DISPUTED_CLAIM"),
    ("5G towers cause COVID-19.", "DISPUTED_CLAIM"),
    ("Humans use only 10% of their brains.", "DISPUTED_CLAIM"),
    ("Climate change is a hoax.", "DISPUTED_CLAIM"),
    ("The moon landing was faked.", "DISPUTED_CLAIM"),
    ("Eating carrots improves night vision dramatically.", "DISPUTED_CLAIM"),
    ("You can neutralize snake venom by drinking alcohol.", "DISPUTED_CLAIM"),
    ("Airplanes spray chemicals to control the population.", "DISPUTED_CLAIM"),
    ("Einstein failed math as a child.", "DISPUTED_CLAIM"),

    ("I think this video is amazing.", "NOT_A_CLAIM"),
    ("This is the best day of my life.", "NOT_A_CLAIM"),
    ("Cats are better than dogs.", "NOT_A_CLAIM"),
    ("I feel like the weather is strange today.", "NOT_A_CLAIM"),
    ("That movie was terrible.", "NOT_A_CLAIM"),
    ("I love how he explains things.", "NOT_A_CLAIM"),
    ("This sounds unbelievable.", "NOT_A_CLAIM"),
    ("Honestly, I don't know what to think anymore.", "NOT_A_CLAIM"),

    ("People say the pyramids were built by aliens.", "DISPUTED_CLAIM"),
    ("Some believe drinking hot water can cure cancer.", "DISPUTED_CLAIM"),
    ("They claim chocolate improves memory, but I'm not sure.", "DISPUTED_CLAIM"),
    ("Research suggests meditation might reduce stress.", "FACTUAL_CLAIM"),
    ("Scientists are still debating the exact cause of autism.", "NOT_A_CLAIM"),
    ("It appears that pollution affects air quality.", "FACTUAL_CLAIM"),

    ("According to NASA, Mars has two moons.", "FACTUAL_CLAIM"),
    ("People often argue that money buys happiness.", "NOT_A_CLAIM"),
    ("There is evidence that dinosaurs had feathers.", "FACTUAL_CLAIM"),
    ("Some say aliens visit Earth regularly.", "DISPUTED_CLAIM"),
    ("The study showed no link between gaming and violence.", "FACTUAL_CLAIM"),
    ("This experiment changed everything for me.", "NOT_A_CLAIM")
]


# ------------------------------
# Run Evaluation
# ------------------------------

def evaluate():
    print("Loading classifier...\n")
    classifier = load_claim_classifier()

    total = len(TEST_DATA)
    correct = 0

    confusion = {
        "FACTUAL_CLAIM": {"correct": 0, "wrong": 0},
        "DISPUTED_CLAIM": {"correct": 0, "wrong": 0},
        "NOT_A_CLAIM": {"correct": 0, "wrong": 0},
    }

    print("\n=== BEGIN EVALUATION ===\n")

    for text, expected in TEST_DATA:
        predicted, score = classifier.predict(text)

        pass_fail = "PASS" if predicted == expected else "FAIL"

        print(f"Text: {text}")
        print(f"Expected: {expected}")
        print(f"Predicted: {predicted} (score={score:.4f})  →  {pass_fail}")
        print("-" * 60)

        if predicted == expected:
            correct += 1
            confusion[expected]["correct"] += 1
        else:
            confusion[expected]["wrong"] += 1

    accuracy = correct / total * 100

    print("\n=== FINAL SUMMARY ===")
    print(f"Total Sentences: {total}")
    print(f"Correct: {correct}")
    print(f"Accuracy: {accuracy:.2f}%\n")

    print("=== CONFUSION REPORT ===")
    print(json.dumps(confusion, indent=4))


if __name__ == "__main__":
    evaluate()
