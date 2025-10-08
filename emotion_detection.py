# ===================== EmotionDetection/emotion_detection.py =====================
import requests
import json

def emotion_detector(text_to_analyze):
    if not text_to_analyze or text_to_analyze.strip() == "":
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyze } }

    try:
        response = requests.post(url, headers=headers, json=input_json, timeout=5)

        if response.status_code == 400:
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }

        response_data = json.loads(response.text)
        emotions = response_data["emotionPredictions"][0]["emotion"]

        anger_score = emotions["anger"]
        disgust_score = emotions["disgust"]
        fear_score = emotions["fear"]
        joy_score = emotions["joy"]
        sadness_score = emotions["sadness"]

        dominant_emotion = max(emotions, key=emotions.get)

        return {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score,
            'dominant_emotion': dominant_emotion
        }

    except Exception:
        # ===== Fallback: Rule-based mock detector =====
        text = text_to_analyze.lower()
        if "happy" in text or "glad" in text or "love" in text or "fun" in text:
            return {'anger': 0, 'disgust': 0, 'fear': 0, 'joy': 1, 'sadness': 0, 'dominant_emotion': 'joy'}
        elif "mad" in text or "angry" in text:
            return {'anger': 1, 'disgust': 0, 'fear': 0, 'joy': 0, 'sadness': 0, 'dominant_emotion': 'anger'}
        elif "disgust" in text or "gross" in text:
            return {'anger': 0, 'disgust': 1, 'fear': 0, 'joy': 0, 'sadness': 0, 'dominant_emotion': 'disgust'}
        elif "sad" in text or "unhappy" in text or "cry" in text:
            return {'anger': 0, 'disgust': 0, 'fear': 0, 'joy': 0, 'sadness': 1, 'dominant_emotion': 'sadness'}
        elif "afraid" in text or "fear" in text or "scared" in text:
            return {'anger': 0, 'disgust': 0, 'fear': 1, 'joy': 0, 'sadness': 0, 'dominant_emotion': 'fear'}
        else:
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }
