from flask import Flask, request, Response, jsonify, session
from flask_cors import CORS, cross_origin
from flask_session import Session  # Import Session
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
app.config['SESSION_TYPE'] = 'filesystem' # use file system to store session data
app.config['SESSION_COOKIE_SECURE'] = True  # if your app is running on https
sess = Session(app)
# Use a dictionary to store chat histories, keyed by session ID
chat_histories = {}
cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')
os.makedirs(cache_dir, exist_ok=True)
app.config['SESSION_FILE_DIR'] = cache_dir
@app.before_request
def make_session_permanent():
    session.permanent = True  # make the session permanent so it lasts beyond a single request


@app.route('/upload', methods=['POST'])
def upload():
    print('Received request')

    if 'audioData' not in request.files:
        print('No audio part')
        return Response('No audio part in the request', status=400)

    file = request.files['audioData']
    audio_bytes = file.read()
    input_text, response_text, cuid = handle_user_audio_input(audio_bytes)
    session_id = session.sid  # get the session ID
    store_message(session_id, 'user', input_text)
    store_message(session_id, 'assistant', response_text)
    response_audio = text_to_audio_data(response_text, cuid)
    ##play_audio(response_audio)
    response_audio_base64 = base64.b64encode(response_audio).decode('utf-8')
    response = {
        'text': response_text,
        'audio': response_audio_base64
    }
    return jsonify(response)

@app.route('/story', methods=['POST'])
def story():
    session_id = session.sid  # get the session ID
    messages = retrieve_messages(session.sid)
    print("messages: ", messages)
    """
    story_text, story_audio = generate_story(messages)
    story_audio_base64 = base64.b64encode(story_audio).decode('utf-8')
    print(story_text)
    response = {
        'text': story_text,
        'audio': story_audio_base64
    }
    return jsonify(response)
    """
    return Response("Not implemented", status=501)

def generate_story(messages):
    story_text = tell_a_story(messages)
    story_audio = text_to_audio_data(story_text)
    return story_text, story_audio


def store_message(session_id ,role, content):
    if session_id not in chat_histories:
        chat_histories[session_id] = []  # create a new chat history if it doesn't exist

    chat_histories[session_id].append({
        role: content
    })


def retrieve_messages(session_id):
    return chat_histories.get(session_id, [])

## for debugging
def play_audio(audio_data: bytes):
    with io.BytesIO(audio_data) as f:
        audio_segment = AudioSegment.from_file(f)
        play(audio_segment)

if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    app.run(port=8080)
