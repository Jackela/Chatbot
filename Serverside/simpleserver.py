from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
from audiotextprocess import audio_data_to_text
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
cors = CORS(app)

import os

@app.route('/upload', methods=['POST'])
@cross_origin()
def upload():
    print('Received request')

    if 'audioData' not in request.files:
        print('No audio part')
        return Response('No audio part in the request', status=400)

    file = request.files['audioData']
    
    filename = secure_filename(file.filename)
    audio_format = filename.rsplit('.', 1)[1].lower() if '.' in filename else None
    sample_rate = request.form.get('sampleRate')
    # Save the file
    current_directory = os.path.dirname(os.path.realpath(__file__))
    save_path = os.path.join(current_directory, filename)
    file.save(save_path)
    print(f"File saved at {save_path}")

    # Reopen the file and read the audio data
    with open(save_path, 'rb') as f:
        audio_data = f.read()

    print(f"Received audio data of type: {audio_format}, sample rate: {sample_rate} and size: {len(audio_data)} bytes.")
    text = audio_data_to_text(audio_data = audio_data, format=audio_format)
    print(text)
    return Response('OK', status=200)

if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    app.run(port=8080)
