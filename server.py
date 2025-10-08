# ===================== server.py =====================
from flask import Flask, request, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/emotionDetector", methods=["GET"])
def detect_emotion():
    text_to_analyze = request.args.get("textToAnalyze") or request.args.get("text")
    try:
        result = emotion_detector(text_to_analyze)
        if result["dominant_emotion"] is None:
            return "Invalid text! Please try again!"
        response_text = (
            f"For the given statement, the system response is "
            f"'anger': {result['anger']}, "
            f"'disgust': {result['disgust']}, "
            f"'fear': {result['fear']}, "
            f"'joy': {result['joy']} and "
            f"'sadness': {result['sadness']}. "
            f"The dominant emotion is {result['dominant_emotion']}."
            f" (Source: {result.get('source', 'unknown')})"
        )
        return response_text
    except Exception as e:
        return f"Error: {str(e)}"



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
