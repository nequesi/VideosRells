import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ImageClip
from moviepy.config import change_settings
from PIL import Image

# Compatibilidade com Pillow >= 10.0
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

# Configura o caminho para o ImageMagick
change_settings({
    "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
})

def adicionar_legenda_no_video(caminho_video_entrada, caminho_video_saida):
    video = VideoFileClip(caminho_video_entrada)
    duracao = video.duration
    metade = duracao / 2

    largura, altura = video.size
    margem_horizontal = 40

    # 🎯 Legenda inferior (embaixo)
    texto_inferior = "#g4educacao\n@g4educacao @tallisgomes @alfredosoares @bruno.nardon"
    legenda_inferior = TextClip(
        texto_inferior,
        fontsize=38,
        color='white',
        font="Arial",
        method='caption',
        size=(largura - margem_horizontal * 2, None)
    ).set_duration(duracao).set_position(("center", altura - 210))

    posicao_vertical = altura * 0.55

    # 📖 Versículos
    texto_topo_1 = 'Êxodo 20:9:\n"Seis dias trabalharás, e farás toda a tua obra.  @ulfrlobo"'
    versiculo_1 = TextClip(
        texto_topo_1,
        fontsize=36,
        color='white',
        font="Arial",
        method='caption',
        size=(largura - margem_horizontal * 2, None)
    ).set_duration(metade).set_position(("center", posicao_vertical))

    texto_topo_2 = 'Provérbios 10:4:\n"A mão preguiçosa empobrece, mas a mão dos diligentes enriquece  @ulfrlobo"'
    versiculo_2 = TextClip(
        texto_topo_2,
        fontsize=36,
        color='white',
        font="Arial",
        method='caption',
        size=(largura - margem_horizontal * 2, None)
    ).set_start(metade).set_duration(metade).set_position(("center", posicao_vertical))

    # 📌 Marca d'água (canto superior direito, mais abaixo)
    marca_dagua = TextClip(
        "@ulfrlobo",
        fontsize=26,
        color='white',
        font="Arial-Bold"
    ).set_duration(duracao).set_position((largura - 180, 60))  # ↓ estava 20, agora 60px do topo

    # ❤️ Ícone de curtida (maior e logo abaixo da marca d’água)
    icone_like = ImageClip(r"D:\Fabrica de cortes\imagem\curte.jpeg") \
        .set_duration(2) \
        .set_start(duracao - 2) \
        .resize(height=100) \
        .set_position((largura - 170, 100))  # ↓ estava 60, agora mais para baixo

    # 🎬 Junta tudo
    video_final = CompositeVideoClip([
        video,
        legenda_inferior,
        versiculo_1,
        versiculo_2,
        marca_dagua,
        icone_like
    ])

    video_final.write_videofile(
        caminho_video_saida,
        codec="libx264",
        audio_codec="aac"
    )

if __name__ == "__main__":
    caminho_entrada = r"D:\Fabrica de cortes\G4\conteudo\corte2.mp4"
    caminho_saida = r"D:\Fabrica de cortes\G4\conteudosFormatados\video2_com_regra.mp4"

    adicionar_legenda_no_video(caminho_entrada, caminho_saida)
