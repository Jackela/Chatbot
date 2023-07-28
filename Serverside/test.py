import wave
import os

file_name = "audio.wav"
current_directory = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(current_directory, file_name)
# Open the file as a WAV file
with wave.open(file_path, 'rb') as wf:
    # Get the number of audio channels (mono=1, stereo=2)
    channels = wf.getnchannels()

    # Print the number of channels
    print(f'Number of channels: {channels}')

    # Get other properties if you're interested
    frame_rate = wf.getframerate()
    sample_width = wf.getsampwidth()
    num_frames = wf.getnframes()

    print(f'Frame rate: {frame_rate}')
    print(f'Sample width: {sample_width}')
    print(f'Number of frames: {num_frames}')
