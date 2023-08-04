from flask import Flask, request, Response, jsonify, session
from flask_cors import CORS, cross_origin
from audiotextprocess import audio_data_to_text, text_to_audio_data
from werkzeug.utils import secure_filename
from chatbotbaidu import handle_user_audio_input, handle_user_text_input, tell_a_story
from pydub import AudioSegment
from pydub.playback import play
import base64
import io
import os

app = Flask(__name__)
app.secret_key = "secret_key"
app.config['SESSION_COOKIE_SECURE'] = False  # if your app is running on https

@app.route('/upload', methods=['POST'])
def upload():
    print('Received request')

    if 'audioData' not in request.files:
        print('No audio part')
        return Response('No audio part in the request', status=400)

    file = request.files['audioData']
    audio_bytes = file.read()
    input_text, response_text, cuid = handle_user_audio_input(audio_bytes)
    store_message('user', input_text)
    store_message('assistant', response_text)
    print(response_text)
    response_audio = text_to_audio_data(response_text, cuid)
    ##play_audio(response_audio)
    response_audio_base64 = base64.b64encode(response_audio).decode('utf-8')
    
    response = {
        'text': response_text,
        'audio': response_audio_base64
    }
    print(retrieve_messages())  
    return jsonify(response)

@app.route('/story', methods=['POST'])
def story():
    messages = retrieve_messages()
    story_text, story_audio = generate_story(messages)
    story_audio_base64 = base64.b64encode(story_audio).decode('utf-8')
    print(story_text)
    response = {
        'text': story_text,
        'audio': story_audio_base64
    }
    return jsonify(response)

def generate_story(messages):
    story_text = tell_a_story(messages)
    story_audio = text_to_audio_data(story_text)
    return story_text, story_audio


def store_message(role, content):
    if 'messages' not in session:
        session['messages'] = []
    session['messages'].append({
        'role': role,
        'content': content
    })

    session.modified = True


def retrieve_messages():
    print(session)
    result = session.get('messages', [])
    return result


## for debugging
def play_audio(audio_data: bytes):
    with io.BytesIO(audio_data) as f:
        audio_segment = AudioSegment.from_file(f)
        play(audio_segment)
if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    app.run(port=8080)
