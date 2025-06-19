from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip
from moviepy.config import change_settings
from PIL import Image
import os

# Compatibilidade Pillow >= 10.0
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

change_settings({
    "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
})

def criar_video_com_margens_de_seguranca():
    caminho = r"D:\Fabrica de cortes\G4"

    especialista = VideoFileClip(os.path.join(caminho, "um_case_sucesso.mp4"))
    satisfatorio = VideoFileClip(os.path.join(caminho, "satisfatorio_gelo.mp4"))

    # 🎯 Resolução final: 1080x1920
    output_width = 1080
    output_height = 1920

    # 🧱 Definindo áreas com segurança visual
    margem_topo = 250
    margem_base = 250
    altura_especialista = 800
    altura_satisfatorio = 620

    duracao = especialista.duration

    # 🔄 Repete satisfatório e remove áudio
    satisfatorio_loop = satisfatorio.without_audio().loop(duration=duracao).subclip(0, duracao)

    # 📏 Redimensiona vídeos
    especialista_resized = especialista.resize(height=altura_especialista).set_position(("center", margem_topo))
    satisfatorio_resized = satisfatorio_loop.resize(height=altura_satisfatorio).set_position(("center", margem_topo + altura_especialista))

    # 🖤 Plano de fundo preto com altura total (incluindo margens)
    background = ColorClip(size=(output_width, output_height), color=(0, 0, 0)).set_duration(duracao)

    # 🎬 Composição final com áudio do especialista
    video_final = CompositeVideoClip(
        [background, especialista_resized, satisfatorio_resized],
        size=(output_width, output_height)
    ).set_duration(duracao).set_audio(especialista.audio)

    saida = os.path.join(caminho, "video_final_com_margens.mp4")

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
    criar_video_com_margens_de_seguranca()
