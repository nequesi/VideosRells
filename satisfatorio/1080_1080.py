from moviepy.editor import VideoFileClip, clips_array
from moviepy.config import change_settings
from PIL import Image
import os

# Compatível com Pillow >= 10.0
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

# Caminho do ImageMagick (usado por moviepy em algumas situações)
change_settings({
    "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
})

def criar_video_1080x1080_empilhado():
    caminho = r"D:\Fabrica de cortes\G4"
    especialista = VideoFileClip(os.path.join(caminho, "especialista.mp4"))
    satisfatorio = VideoFileClip(os.path.join(caminho, "satisfatorio.mp4"))

    # Usa apenas a duração do vídeo do especialista
    duracao_esp = especialista.duration
    satisfatorio_cortado = satisfatorio.subclip(0, duracao_esp)

    # Redimensiona cada vídeo para 1080x540
    especialista_resized = especialista.resize(height=540).resize(width=1080)
    satisfatorio_resized = satisfatorio_cortado.resize(height=540).resize(width=1080)

    # Empilha os vídeos verticalmente -> 1080x1080
    video_final = clips_array([
        [especialista_resized],
        [satisfatorio_resized]
    ], bg_color=None)

    saida = os.path.join(caminho, "video_final_1080x1080.mp4")
    video_final.write_videofile(
        saida,
        codec="libx264",
        audio_codec="aac",
        preset="fast",
        threads=4,
        ffmpeg_params=["-movflags", "+faststart"]
    )

if __name__ == "__main__":
    criar_video_1080x1080_empilhado()
