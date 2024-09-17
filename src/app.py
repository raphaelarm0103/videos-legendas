import whisper
import ffmpeg
import srt
from datetime import timedelta
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.config import change_settings
import pysrt

# Configurar o caminho do ImageMagick
change_settings({"IMAGEMAGICK_BINARY": "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})


# Passo 1: Transcrição do áudio usando Whisper
def transcrever_audio(audio_file):
    model = whisper.load_model("medium")
    result = model.transcribe(audio_file, language='pt', temperature=0.0)
    return result['segments']


# Passo 2: Criação do arquivo SRT com timestamps e texto
def criar_legenda_srt(segments, srt_file):
    subtitles = []
    for i, segment in enumerate(segments):
        start = timedelta(seconds=segment['start'])
        end = timedelta(seconds=segment['end'])
        content = segment['text'].strip()
        subtitles.append(srt.Subtitle(index=i + 1, start=start, end=end, content=content))

    with open(srt_file, 'w', encoding='utf-8') as file:
        file.write(srt.compose(subtitles))


# Passo 3: Adicionar a legenda ao vídeo original com MoviePy
def embutir_legenda_moviepy(video_input_path, srt_path, output_path, sync_offset=0.0):
    # Carregar o vídeo original
    video = VideoFileClip(video_input_path)
    # Carregar as legendas do arquivo .srt
    subs = pysrt.open(srt_path, encoding='utf-8')

    # Função para converter tempo do SRT para segundos
    def srt_to_seconds(time):
        return time.hours * 3600 + time.minutes * 60 + time.seconds + time.milliseconds / 1000

    # Criar clipes de texto para cada legenda
    subtitles_clips = []
    for sub in subs:
        start_time = max(0, srt_to_seconds(sub.start) + sync_offset)
        end_time = srt_to_seconds(sub.end) + sync_offset
        # Criar um clipe de texto com a legenda
        txt_clip = TextClip(sub.text, fontsize=80, color='white', size=(video.w - 50, None), method='caption',
                            align='center', bg_color='VioletRed1')
        txt_clip = txt_clip.set_position(('center', video.h - 100)).set_start(start_time).set_duration(
            end_time - start_time)
        subtitles_clips.append(txt_clip)

    # Combinar o vídeo com os clipes de legendas
    final_clip = CompositeVideoClip([video] + subtitles_clips)

    # Exportar o vídeo final com as legendas embutidas
    final_clip.write_videofile(output_path, codec='libx264', fps=video.fps)


# Caminhos dos arquivos
video_input = r'C:\Users\phael\Documents\Videos\VIDEO_ANGELA_VALE_DO_ARAGUAIA.mp4'
audio_file = r'C:\Users\phael\Documents\Videos\audio.wav'
srt_file = r'C:\Users\phael\Documents\Videos\legenda.srt'
video_output = r'C:\Users\phael\Documents\Videos\arquivo.mp4'

# Extração do áudio
ffmpeg.input(video_input).output(audio_file).run(overwrite_output=True)

# Transcrição e criação da legenda
segments = transcrever_audio(audio_file)
criar_legenda_srt(segments, srt_file)

sync_offset = -0.5  # Por exemplo, -0.5 para adiantar a legenda em 0.5 segundos

# Embutir legenda no vídeo usando MoviePy
embutir_legenda_moviepy(video_input, srt_file, video_output)
# print(b'\n'.join(TextClip.list('color')).decode())
print("Legendas adicionadas com sucesso ao vídeo!")


