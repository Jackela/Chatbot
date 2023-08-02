from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
cors = CORS(app)

@app.route('/upload', methods=['POST'])
@cross_origin()
def upload():
    print('Received request')

    # Read the audio data from the form data
    audio_data = request.files.get('audioData')

    if not audio_data:
        print('No audio data')
        return Response('No audio data in the request', status=400)

    # Save the audio data to a file
    current_directory = os.path.dirname(os.path.realpath(__file__))
    save_path = os.path.join(current_directory, 'audio.wav')
    audio_data.save(save_path)

    print(f"File saved at {save_path}")
    print(f"Received audio data.")
    
    return Response('OK', status=200)


if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    app.run(port=8080)
