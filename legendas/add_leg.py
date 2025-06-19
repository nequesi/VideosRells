from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

# (Se quiser, pode também definir via os.environ aqui — mas não é obrigatório quando usa change_settings)

def adicionar_legenda_no_video(entrada, saida):

    video = VideoFileClip(entrada)
    texto = "#g4educacao\n@g4educacao @tallisgomes @alfredosoares @bruno.nardon"
    legenda = TextClip(texto, fontsize=40, color='white', font='Arial', method='caption', size=video.size)
    legenda = legenda.set_duration(video.duration).set_position(("center", "bottom"))
    video_com_legenda = CompositeVideoClip([video, legenda])
    video_com_legenda.write_videofile(saida, codec="libx264", audio_codec="aac")

if __name__ == "__main__":
    entrada = r"C:\Users\walhe\Documents\pythonProject\corte1.mp4"
    saida = r"C:\Users\walhe\Documents\pythonProject\video1_com_regra.mp4"
    adicionar_legenda_no_video(entrada, saida)
