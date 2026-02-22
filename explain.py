from defect_knowledge import DEFECT_INFO
import ollama


# ✅ ADD THIS BACK
def classify_weld(detections):
    if len(detections) == 0:
        return "Good Weld"
    return "Bad Weld"


def generate_explanation(defect, confidence):
    info = DEFECT_INFO.get(defect)

    if not info:
        return "No detailed explanation available for this defect."

    return f"""
Detected Defect: {defect}
Confidence: {confidence}

What it means:
{info['meaning']}

Why it occurs:
{info['cause']}

Weld acceptability:
{info['acceptability']}
"""
