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

def criar_video_vertical_720x1280():
    caminho = r"D:\Fabrica de cortes\G4"

    especialista = VideoFileClip(os.path.join(caminho, "um_case_sucesso.mp4"))
    satisfatorio = VideoFileClip(os.path.join(caminho, "satisfatorio_gelo.mp4"))

    # 🎯 Resolução final: 720x1280 (vertical)
    output_width = 720
    output_height = 1280

    # 🔧 Porcentagens de altura
    altura_especialista_pct = 0.60
    altura_satisfatorio_pct = 0.40

    altura_especialista = int(output_height * altura_especialista_pct)
    altura_satisfatorio = output_height - altura_especialista
    duracao = especialista.duration

    especialista_resized = especialista.resize(height=altura_especialista)
    especialista_resized = especialista_resized.set_position(("center", 0))

    satisfatorio_loop = satisfatorio.without_audio().loop(duration=duracao).subclip(0, duracao)
    satisfatorio_resized = satisfatorio_loop.resize(height=altura_satisfatorio)
    satisfatorio_resized = satisfatorio_resized.set_position(("center", altura_especialista))

    video_final = CompositeVideoClip(
        [especialista_resized, satisfatorio_resized],
        size=(output_width, output_height)
    ).set_duration(duracao).set_audio(especialista.audio)

    saida = os.path.join(caminho, "video_final_720x1280.mp4")

    video_final.write_videofile(
        saida,
        codec="libx264",
        audio_codec="aac",
        preset="fast",
        threads=4,
        ffmpeg_params=["-movflags", "+faststart"]
    )

    especialista.reader.close()
    if especialista.audio:
        especialista.audio.reader.close_proc()
    satisfatorio.reader.close()
    if satisfatorio.audio:
        satisfatorio.audio.reader.close_proc()

if __name__ == "__main__":
    criar_video_vertical_720x1280()
