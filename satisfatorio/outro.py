from moviepy.editor import VideoFileClip, clips_array
from moviepy.config import change_settings
from PIL import Image
import os

# Compatibilidade Pillow >= 10.0
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

change_settings({
    "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
})

def criar_video_sem_loop():
    caminho = r"D:\Fabrica de cortes\G4"
    especialista = VideoFileClip(os.path.join(caminho, "especialista.mp4"))
    satisfatorio = VideoFileClip(os.path.join(caminho, "satisfatorio.mp4"))

    output_width = 1280
    output_height = 720
    video_height = output_height // 2

    duracao_esp = especialista.duration

    # 🔪 Corta os primeiros 2 minutos do satisfatório e limita à duração do especialista
    satisfatorio_cortado = satisfatorio.subclip(0, duracao_esp)

    def resize_crop(clip, width, height):
        clip_resized = clip.resize(width=width)
        if clip_resized.h < height:
            clip_resized = clip.resize(height=height)
        y_crop = max(0, (clip_resized.h - height) / 2)
        return clip_resized.crop(y1=y_crop, y2=y_crop + height)

    especialista_resized = especialista
    satisfatorio_resized = resize_crop(satisfatorio_cortado, output_width, video_height)

    video_final = clips_array([[especialista_resized],
                               [satisfatorio_resized]],
                              bg_color=None)

    saida = os.path.join(caminho, "video_final_split_sem_loop.mp4")
    video_final.write_videofile(
        saida,
        codec="libx264",
        audio_codec="aac",
        preset="fast",
        threads=4,
        ffmpeg_params=["-movflags", "+faststart"]
    )

if __name__ == "__main__":
    criar_video_sem_loop()