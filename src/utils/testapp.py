# Usando raw string para evitar problemas com caracteres de escape
video_input = r'C:\Users\phael\Documents\Videos\VIDEO_ANGELA_VALE_DO_ARAGUAIA.mp4'

# Seu código para processar o vídeo
import ffmpeg

# Tente executar o processo para ver se o caminho agora é aceito corretamente
try:
    ffmpeg.input(video_input).output('audio.wav').run(overwrite_output=True)
    print("Áudio extraído com sucesso.")
except Exception as e:
    print(f"Erro ao processar o vídeo: {e}")
