from flask import Flask, request, jsonify
from src.processa_audio.audio_processing import AudioProcessor
from src.processa_legenda.subtitle_creation import SubtitleCreator
from src.cria_video_legenda.video_processing import VideoProcessor

app = Flask(__name__)


# Endpoint para transcrever áudio e criar legendas
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    audio_file = request.files['audio']
    audio_processor = AudioProcessor()
    segments = audio_processor.transcribe_audio(audio_file)
    return jsonify(segments)


# Endpoint para criar arquivo SRT
@app.route('/create_srt', methods=['POST'])
def create_srt():
    segments = request.json['segments']
    srt_file_path = request.json['srt_file_path']
    subtitle_creator = SubtitleCreator()
    subtitle_creator.create_word_srt(segments, srt_file_path)
    return jsonify({"message": "SRT file created successfully."})


# Endpoint para embutir legenda no vídeo
@app.route('/embed_subtitle', methods=['POST'])
def embed_subtitle():
    video_input_path = request.json['video_input_path']
    srt_path = request.json['srt_path']
    output_path = request.json['output_path']
    sync_offset = request.json.get('sync_offset', 0.0)
    video_processor = VideoProcessor()
    video_processor.embed_subtitles(video_input_path, srt_path, output_path, sync_offset)
    return jsonify({"message": "Subtitles embedded successfully."})


if __name__ == '__main__':
    app.run(debug=True)
