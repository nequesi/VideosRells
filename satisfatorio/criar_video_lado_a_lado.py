from moviepy.editor import VideoFileClip, CompositeVideoClip
from moviepy.config import change_settings
from PIL import Image
import os

# Compatibilidade Pillow >= 10.0
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

change_settings({
    "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
})

def criar_video_lado_a_lado():
    caminho_especialista = r"D:\Fabrica de cortes\brasil_paralelo\reels_final2"
    caminho = r"D:\Fabrica de cortes\satisfatorio"

    especialista = VideoFileClip(os.path.join(caminho_especialista, "reel_01.mp4"))
    satisfatorio = VideoFileClip(os.path.join(caminho, "foqueira.mp4"))

    # 🎯 Resolução de saída: 1920x1080 (lado a lado → 960x1080 cada)
    output_width = 1920
    output_height = 1080
    half_width = output_width // 2

    duracao = especialista.duration

    # Redimensiona os vídeos para 960x1080 cada
    especialista_resized = especialista.resize(height=output_height).resize(width=half_width)
    especialista_resized = especialista_resized.set_position((0, 0))

    satisfatorio_loop = satisfatorio.without_audio().loop(duration=duracao).subclip(0, duracao)
    satisfatorio_resized = satisfatorio_loop.resize(height=output_height).resize(width=half_width)
    satisfatorio_resized = satisfatorio_resized.set_position((half_width, 0))

    # Combina os dois vídeos lado a lado
    video_final = CompositeVideoClip(
        [especialista_resized, satisfatorio_resized],
        size=(output_width, output_height)
    ).set_duration(duracao).set_audio(especialista.audio)

    saida = os.path.join(caminho_especialista, "video_final_lado_a_lado.mp4")

    video_final.write_videofile(
        saida,
        codec="libx264",
        audio_codec="aac",
        preset="fast",
        threads=4,
        ffmpeg_params=["-movflags", "+faststart"]
    )

    # Encerra corretamente
    especialista.reader.close()
    if especialista.audio:
        especialista.audio.reader.close_proc()
    satisfatorio.reader.close()
    if satisfatorio.audio:
        satisfatorio.audio.reader.close_proc()

if __name__ == "__main__":
    criar_video_lado_a_lado()
