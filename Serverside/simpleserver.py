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
CORS(app)
sess = Session(app)
# Use a dictionary to store chat histories, keyed by session ID
chat_histories = {}
cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')
os.makedirs(cache_dir, exist_ok=True)
app.config['SESSION_FILE_DIR'] = cache_dir

@app.before_request
def make_session_permanent():
    session.permanent = True  # make the session permanent so it lasts beyond a single request

@app.route('/uploadText', methods=['POST'])
def upload_text():
    textData = request.get_json()
    cuid = textData['cuid']
    text = textData['message']
    response = process_text(text, cuid)
    return jsonify(response)
    
@app.route('/uploadAudio', methods=['POST'])
def uploadAudio():
    print('Received request')
    if 'audioData' not in request.files:
        print('No audio part')
        return Response('No audio part in the request', status=400)
    
    file = request.files['audioData']
    cuid = get_cuid(request)
    response = process_audio(file, cuid)
    return jsonify(response)

@app.route('/story', methods=['POST'])
def story():
    data = request.get_json()
    cuid = data['cuid']
    messages = retrieve_messages(cuid)
    story_text, story_audio = generate_story(messages, cuid)
    story_audio_base64 = base64.b64encode(story_audio).decode('utf-8')
    response = {
        'text': story_text,
        'audio': story_audio_base64
    }
    return jsonify(response)



def read_audio(file):
    return file.read()

def get_cuid(request):
    return request.form['cuid']

def encode_audio(response_audio):
    return base64.b64encode(response_audio).decode('utf-8')

def create_response(response_text: str, response_audio_base64):
    return {
        'text': response_text,
        'audio': response_audio_base64
    }

def process_audio(file, cuid):
    audio_bytes = read_audio(file)
    input_text, response_text = handle_user_audio_input(audio_bytes, cuid)
    store_message(cuid, 'user', input_text)
    store_message(cuid, 'assistant', response_text)
    response_audio = text_to_audio_data(response_text, cuid)
    response_audio_base64 = encode_audio(response_audio)
    return create_response(response_text, response_audio_base64)

def process_text(text, cuid):
    response_text = handle_user_text_input(text, cuid)
    store_message(cuid, 'user', text)
    store_message(cuid, 'assistant', response_text)
    response_audio = text_to_audio_data(response_text, cuid)
    response_audio_base64 = encode_audio(response_audio)
    return create_response(response_text, response_audio_base64)

def generate_story(messages, cuid):
    story_text = tell_a_story(messages)
    story_audio = text_to_audio_data(story_text, cuid)
    return story_text, story_audio


def store_message(cuid ,role, content):
    if cuid not in chat_histories:
        chat_histories[cuid] = []  # create a new chat history if it doesn't exist

    chat_histories[cuid].append({
        role: content
    })


def retrieve_messages(cuid):
    return chat_histories.get(cuid, [])

## for debugging
def play_audio(audio_data: bytes):
    with io.BytesIO(audio_data) as f:
        audio_segment = AudioSegment.from_file(f)
        play(audio_segment)

if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    app.run(port=8080)
