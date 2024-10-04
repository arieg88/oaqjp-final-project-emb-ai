import requests
import json

def emotion_detector(text_to_analyze):
    # Check if input is empty
    if not text_to_analyze.strip():
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
    
    # Define the URL and headers
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_data = {"raw_document": {"text": text_to_analyze}}
    
    # Send the POST request to the Watson API
    response = requests.post(url, headers=headers, json=input_data)
    
    # Check for 400 status code or any other failure
    if response.status_code == 400:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
    
    if response.status_code == 200:
        # Parse the response JSON and return the text attribute
        response_data = response.json()
        emotions = response_data['emotionPredictions'][0]['emotion']
        highest_score = 0
        highest_score_emotion = None
        for emotion in emotions:
            if emotions[emotion] > highest_score:
                highest_score = emotions[emotion]
                highest_score_emotion = emotion

        return {
            'anger': emotions['anger'],
            'disgust': emotions['disgust'],
            'fear': emotions['fear'],
            'joy': emotions['joy'],
            'sadness': emotions['sadness'],
            'dominant_emotion': f'{highest_score_emotion}'
        }
    else:
        # Return an error message if the request failed
        return f"Error: {response.status_code} - {response.text}"


# Example usage:
if __name__ == "__main__":
    sample_text = "I love this new technology."
    print(emotion_detector(sample_text))
