"""
This module provides the Flask web server for the Emotion Detection application.

It defines the following routes:
- '/' for serving the index page.
- '/emotionDetector' for processing POST requests and analyzing emotions from text.
"""
from flask import Flask, request, jsonify, render_template
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route('/')
def index():
    """
    Serve the index page for the application.

    Returns:
        Response object containing the rendered index.html page.
    """
    return render_template('index.html')

@app.route('/emotionDetector', methods=['POST'])
def emotion_detector_route():
    """
    Process a POST request to detect emotions in a given text.

    The function expects a JSON payload with a "text" field, which is analyzed
    for emotions using the emotion_detector function.

    Returns:
        JSON object containing the emotions detected in the input text or
        an error message if the input is invalid or if an exception occurs.
    """
    try:
        # Get the input text from the POST request and strip any leading/trailing whitespace
        input_text = request.json.get('text', '').strip()

        # Check if the input is empty and return an error message
        if not input_text:
            return jsonify({"response": "Invalid text! Please try again."}), 400

        # Call the emotion detector function
        emotions = emotion_detector(input_text)

        # Check if the dominant emotion is None (indicating a failed emotion detection)
        if emotions['dominant_emotion'] is None:
            return jsonify({"response": "Invalid text! Please try again."}), 400

        # Format the response string
        response_string = (
            f"For the given statement, the system response is "
            f"'anger': {emotions['anger']}, 'disgust': {emotions['disgust']}, "
            f"'fear': {emotions['fear']}, 'joy': {emotions['joy']}, "
            f"and 'sadness': {emotions['sadness']}. "
            f"The dominant emotion is {emotions['dominant_emotion']}."
        )

        return jsonify({"response": response_string})

    except (KeyError, ValueError) as error:
        # Catch specific exceptions and return a meaningful error message
        return jsonify({"error": f"Invalid input: {str(error)}"}), 400

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
