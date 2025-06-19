from moviepy.editor import VideoFileClip, clips_array, ColorClip
from moviepy.config import change_settings
from PIL import Image
import os

# Compatibilidade Pillow >= 10.0
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

change_settings({
    "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
})

def criar_video_para_reels():
    caminho = r"D:\Fabrica de cortes\G4"

    especialista = VideoFileClip(os.path.join(caminho, "um_case_sucesso.mp4"))
    satisfatorio = VideoFileClip(os.path.join(caminho, "satisfatorio_gelo.mp4"))

    output_width = 1080
    output_height = 1920

    duracao_esp = especialista.duration

    # Loop no satisfatório e remove o áudio
    satisfatorio_loop = satisfatorio.without_audio().loop(duration=duracao_esp + 0.5).subclip(0, duracao_esp)

    # Altura fixa para o especialista (ex: 75%) e satisfatório com 25%
    altura_especialista = int(output_height * 0.70)  # vídeo de cima (mantém)
    altura_satisfatorio = output_height - altura_especialista  # vídeo de baixo (reduzido)

    def resize_and_crop(clip, target_width, target_height):
        clip_resized = clip.resize(width=target_width)
        if clip_resized.h < target_height:
            clip_resized = clip.resize(height=target_height)
        y_crop = max(0, (clip_resized.h - target_height) / 2)
        return clip_resized.crop(y1=y_crop, y2=y_crop + target_height)

    especialista_resized = resize_and_crop(especialista, output_width, altura_especialista)
    satisfatorio_resized = resize_and_crop(satisfatorio_loop, output_width, altura_satisfatorio)

    video_final = clips_array([
        [especialista_resized],
        [satisfatorio_resized]
    ]).set_audio(especialista.audio)

    saida = os.path.join(caminho, "video_final_reels11.mp4")

    video_final.write_videofile(
        saida,
        codec="libx264",
        audio_codec="aac",
        preset="fast",
        threads=4,
        ffmpeg_params=["-movflags", "+faststart"]
    )

if __name__ == "__main__":
    criar_video_para_reels()
