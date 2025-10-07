# emotion_detection.py

import requests
import json

def emotion_detector(text_to_analyze):
    """
    Calls the Watson NLP EmotionPredict API with the provided text.
    Extracts anger, disgust, fear, joy, and sadness scores,
    then finds and returns the dominant emotion.
    """

    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    input_json = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    try:
        response = requests.post(url, headers=headers, json=input_json)
        if response.status_code == 200:
            result = response.json()

            # Extract emotions and scores
            emotions = result['emotionPredictions'][0]['emotion']
            anger = emotions.get('anger', 0)
            disgust = emotions.get('disgust', 0)
            fear = emotions.get('fear', 0)
            joy = emotions.get('joy', 0)
            sadness = emotions.get('sadness', 0)

            # Determine dominant emotion
            scores = {
                'anger': anger,
                'disgust': disgust,
                'fear': fear,
                'joy': joy,
                'sadness': sadness
            }
            dominant_emotion = max(scores, key=scores.get)

            # Return formatted dictionary
            return {
                'anger': anger,
                'disgust': disgust,
                'fear': fear,
                'joy': joy,
                'sadness': sadness,
                'dominant_emotion': dominant_emotion
            }

        else:
            return {"error": f"Request failed with status code {response.status_code}"}

    except Exception as e:
        return {"error": str(e)}
