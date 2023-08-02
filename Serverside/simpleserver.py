from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
from audiotextprocess import audio_data_to_text, text_to_audio_data
from werkzeug.utils import secure_filename
from chatbotbaidu import handle_user_audio_input, handle_user_text_input
from pydub import AudioSegment
from pydub.playback import play
import io
import os

app = Flask(__name__)
cors = CORS(app)


@app.route('/upload', methods=['POST'])
@cross_origin()
def upload():
    print('Received request')

    if 'audioData' not in request.files:
        print('No audio part')
        return Response('No audio part in the request', status=400)

    file = request.files['audioData']
    audio_bytes = file.read()
    response, cuid = handle_user_audio_input(audio_bytes)
    print(response)
    response_audio = text_to_audio_data(response, cuid)
    play_audio(response_audio)
    return Response('Success', status=200)


## for debugging
def play_audio(audio_data: bytes):
    with io.BytesIO(audio_data) as f:
        audio_segment = AudioSegment.from_file(f)
        play(audio_segment)
if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    app.run(port=8080)
