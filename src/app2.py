import pysrt
import whisper
import ffmpeg
import srt
from datetime import timedelta
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.config import change_settings

# Configurar o caminho completo do ImageMagick
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})


# Função para transcrever áudio usando Whisper e obter segmentos detalhados
def transcrever_audio(audio_file):
    model = whisper.load_model("medium")  # Use "medium" ou "large" para mais precisão
    result = model.transcribe(audio_file, language='pt', temperature=0.0, word_timestamps=True)

    # Imprimir detalhes dos segmentos para diagnosticar o que está acontecendo
    print("Segmentos retornados:", result['segments'])
    for segment in result['segments']:
        print(segment)  # Imprime cada segmento detalhadamente

    return result['segments']


# Função para criar arquivo SRT com palavras individuais sincronizadas
def criar_legenda_srt_palavras(segments, srt_file):
    subtitles = []
    index = 1

    # Iterar sobre os segmentos e palavras
    for segment in segments:
        # Verificar se a chave 'words' existe no segmento e tem conteúdo
        if 'words' in segment and segment['words']:
            for word in segment['words']:
                # Verificar se as chaves 'start', 'end', e 'text' estão presentes
                if 'start' in word and 'end' in word and 'word' in word:
                    # Converter np.float64 para float
                    start = timedelta(seconds=float(word['start']))
                    end = timedelta(seconds=float(word['end']))
                    content = word['word'].strip()
                    subtitles.append(srt.Subtitle(index=index, start=start, end=end, content=content))
                    index += 1
        else:
            print("Nenhuma palavra encontrada no segmento:", segment)

    # Se não houver legendas, avise
    if not subtitles:
        print("Nenhuma legenda foi gerada. Verifique a estrutura dos segmentos e as palavras.")

    # Salvar as legendas em formato SRT
    with open(srt_file, 'w', encoding='utf-8') as file:
        file.write(srt.compose(subtitles))


def criar_legenda_srt_completa(segments, srt_file):
    subtitles = []
    for i, segment in enumerate(segments):
        start = timedelta(seconds=segment['start'])
        end = timedelta(seconds=segment['end'])
        content = segment['text'].strip()
        subtitles.append(srt.Subtitle(index=i + 1, start=start, end=end, content=content))

    with open(srt_file, 'w', encoding='utf-8') as file:
        file.write(srt.compose(subtitles))


def adjust_fontsize(video_height, scale_factor=0.05):
    # Ajuste o scale_factor conforme necessário
    return int(video_height * scale_factor)


# Função para embutir legenda no vídeo com ajuste de sincronização
def embutir_legenda_moviepy(video_input_path, srt_path, output_path, sync_offset=0.0):
    # Carregar o vídeo original
    video = VideoFileClip(video_input_path)
    video_width, video_height = video.size
    dynamic_fontsize = adjust_fontsize(video_height)
    # Carregar as legendas do arquivo .srt
    subs = pysrt.open(srt_path, encoding='utf-8')

    # Função para converter tempo do SRT para segundos
    def srt_to_seconds(time):
        return time.hours * 3600 + time.minutes * 60 + time.seconds + time.milliseconds / 1000

    # Criar clipes de texto para cada legenda com ajuste de sincronização
    subtitles_clips = []
    for sub in subs:
        # Ajustar o tempo de início e fim das legendas pelo offset fornecido
        start_time = max(0, srt_to_seconds(sub.start) + sync_offset)  # Evita início negativo
        end_time = srt_to_seconds(sub.end) + sync_offset
        # Criar um clipe de texto com a legenda
        txt_clip = TextClip(
            sub.text.upper(),
            fontsize=dynamic_fontsize,
            color='white',
            stroke_color='black',  # Adiciona contorno para melhor visibilidade
            stroke_width=2,
            size=None,
            method='caption',
            align='center',
            # bg_color='SeaGreen',
            font='Impact'
        )

        vertical_offset_factor = 0.1
        vertical_position = video.h - int(video.h * vertical_offset_factor)
        # Ajustar a posição na parte inferior do vídeo
        txt_clip = txt_clip.set_position(('center', vertical_position)).set_start(start_time).set_duration(
            end_time - start_time
        )
        subtitles_clips.append(txt_clip)

    # Combinar o vídeo com os clipes de legendas
    final_clip = CompositeVideoClip([video] + subtitles_clips)

    # Exportar o vídeo final com as legendas embutidas
    final_clip.write_videofile(output_path, codec='libx264', fps=video.fps)


# Caminhos dos arquivos
video_input = r'C:\Users\phael\Documents\Videos\Video-reuniao.mp4'
audio_file = r'C:\Users\phael\Documents\Videos\audio.wav'
srt_file = r'C:\Users\phael\Documents\Videos\legenda_palavras.srt'
video_output = r'C:\Users\phael\Documents\Videos\Video-reuniao-legenda.mp4'

# Extração do áudio
ffmpeg.input(video_input).output(audio_file).run(overwrite_output=True)

# Transcrição e criação da legenda por palavras
segments = transcrever_audio(audio_file)
criar_legenda_srt_palavras(segments, srt_file)

# Ajuste o valor de sync_offset para sincronizar a legenda com a fala (em segundos)
sync_offset = 0.0  # Ajuste conforme necessário para sincronização

# Embutir legenda no vídeo usando MoviePy com ajuste de sincronização
embutir_legenda_moviepy(video_input, srt_file, video_output, sync_offset=sync_offset)

print("Legendas sincronizadas por palavra adicionadas com sucesso ao vídeo!")
