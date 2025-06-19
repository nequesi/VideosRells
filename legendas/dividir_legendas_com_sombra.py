import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ImageClip
from moviepy.config import change_settings
from PIL import Image

# Compatibilidade com Pillow >= 10.0
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

# Configurar o caminho do ImageMagick
change_settings({
    "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
})

def adicionar_legendas_duas_fases(video, largura, altura, duracao_parte):
    margem_horizontal = 40
    posicao_vertical = altura * 0.55
    metade = duracao_parte / 2

    texto_inferior1 = "#g4educacao\n@g4educacao @tallisgomes @alfredosoares @bruno.nardon"
    texto_inferior = "#g4educacao\n@g4.educacao | @tallisgomes | @alfredosoaresoficial | @brunonardon"  # tiktok

    # Sombra da legenda inferior
    sombra_inferior = TextClip(
        texto_inferior,
        fontsize=38,
        color='black',
        font="Arial",
        method='caption',
        size=(largura - margem_horizontal * 2, None)
    ).set_duration(duracao_parte).set_position(("center", altura - 148))

    # Texto branco por cima
    legenda_inferior = TextClip(
        texto_inferior,
        fontsize=38,
        color='white',
        font="Arial",
        method='caption',
        size=(largura - margem_horizontal * 2, None)
    ).set_duration(duracao_parte).set_position(("center", altura - 150))

    # Versículo 1 com sombra
    texto_topo_1 = 'Êxodo 20:9:\n"Seis dias trabalharás, e farás toda a tua obra."'
    sombra_verso_1 = TextClip(
        texto_topo_1,
        fontsize=36,
        color='black',
        font="Arial",
        method='caption',
        size=(largura - margem_horizontal * 2, None)
    ).set_duration(metade).set_position(("center", posicao_vertical + 2))

    versiculo_1 = TextClip(
        texto_topo_1,
        fontsize=36,
        color='white',
        font="Arial",
        method='caption',
        size=(largura - margem_horizontal * 2, None)
    ).set_duration(metade).set_position(("center", posicao_vertical))

    # Versículo 2 com sombra
    texto_topo_2 = 'Provérbios 10:4:\n"A mão preguiçosa empobrece, mas a mão dos diligentes enriquece"'
    sombra_verso_2 = TextClip(
        texto_topo_2,
        fontsize=36,
        color='black',
        font="Arial",
        method='caption',
        size=(largura - margem_horizontal * 2, None)
    ).set_start(metade).set_duration(metade).set_position(("center", posicao_vertical + 2))

    versiculo_2 = TextClip(
        texto_topo_2,
        fontsize=36,
        color='white',
        font="Arial",
        method='caption',
        size=(largura - margem_horizontal * 2, None)
    ).set_start(metade).set_duration(metade).set_position(("center", posicao_vertical))

    # Marca d'água fixa no canto superior direito
    texto_marca_dagua = "@ulfrlobo"
    marca_dagua = TextClip(
        texto_marca_dagua,
        fontsize=26,
        color='white',
        font="Arial-Bold"
    ).set_duration(duracao_parte).set_position((largura - 180, 30))  # 30px do topo

    # Ícone nos últimos 2 segundos
    caminho_icone_like = r"D:\Fabrica de cortes\imagem\curte.jpeg"  # ajuste caminho se necessário
    icone_like = ImageClip(caminho_icone_like).set_duration(2).set_start(duracao_parte - 2)
    icone_like = icone_like.resize(height=80).set_position((largura - 170, 70))

    return CompositeVideoClip([
        video,
        sombra_inferior, legenda_inferior,
        sombra_verso_1, versiculo_1,
        sombra_verso_2, versiculo_2,
        marca_dagua,
        icone_like
    ])

def dividir_em_sete_partes_com_legendas(caminho_entrada, caminho_saida_base):
    video = VideoFileClip(caminho_entrada)
    duracao_total = video.duration
    duracao_parte = duracao_total / 7

    for i in range(7):
        inicio = i * duracao_parte
        fim = inicio + duracao_parte

        subclip = video.subclip(inicio, fim)
        largura, altura = subclip.size

        video_legendas = adicionar_legendas_duas_fases(subclip, largura, altura, duracao_parte)

        caminho_saida = f"{caminho_saida_base}_parte_{i+1}.mp4"
        print(f"Exportando: {caminho_saida}")
        video_legendas.write_videofile(
            caminho_saida,
            codec="libx264",
            audio_codec="aac"
        )

if __name__ == "__main__":
    caminho_entrada = r"D:\Fabrica de cortes\G4\conteudo\corte1.mp4"
    caminho_saida_base = r"D:\Fabrica de cortes\G4\conteudosFormatados\tiktok\video"

    dividir_em_sete_partes_com_legendas(caminho_entrada, caminho_saida_base)
