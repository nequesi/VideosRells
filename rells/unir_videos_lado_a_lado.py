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
    caminho = r"D:\Fabrica de cortes\G4"

    satisfatorio = VideoFileClip(os.path.join(caminho, "satisfatorio_gelo.mp4")).without_audio()
    especialista = VideoFileClip(os.path.join(caminho, "um_case_sucesso.mp4"))

    # 🎯 Resolução final: 1920x1080
    output_width = 1920
    output_height = 1080

    duracao = especialista.duration

    # 🔁 Loop do satisfatório para durar o mesmo tempo
    satisfatorio_loop = satisfatorio.loop(duration=duracao).subclip(0, duracao)

    # Redimensionar vídeos para altura desejada
    especialista_resized = especialista.resize(height=output_height)
    satisfatorio_resized = satisfatorio_loop.resize(height=output_height)

    # Posicionar vídeos lado a lado
    metade_largura = output_width // 2

    especialista_resized = especialista_resized.set_position((metade_largura, "center"))
    satisfatorio_resized = satisfatorio_resized.set_position((0, "center"))

    # Cria o vídeo final lado a lado
    video_final = CompositeVideoClip(
        [satisfatorio_resized, especialista_resized],
        size=(output_width, output_height)
    ).set_duration(duracao).set_audio(especialista.audio)

    saida = os.path.join(caminho, "video_final_lado_a_lado_1920x1080.mp4")

    video_final.write_videofile(
        saida,
        codec="libx264",
        audio_codec="aac",
        preset="fast",
        threads=4,
        ffmpeg_params=["-movflags", "+faststart"]
    )

    # Libera recursos
    especialista.reader.close()
    if especialista.audio:
        especialista.audio.reader.close_proc()
    satisfatorio.reader.close()
    if satisfatorio.audio:
        satisfatorio.audio.reader.close_proc()

if __name__ == "__main__":
    criar_video_lado_a_lado()
