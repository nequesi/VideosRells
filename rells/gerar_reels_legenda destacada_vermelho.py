from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ImageClip, ColorClip
from moviepy.config import change_settings
from moviepy.video.fx.fadein import fadein
from PIL import Image
import os

if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

change_settings({
    "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
})

def gerar_reels(video_path, srt_path, pasta_saida, largura=960, altura=540, fonte='Arial-Bold'):
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    video = VideoFileClip(video_path)

    banner_transparente = r"D:\Fabrica de cortes\G4\alfredo\banner_rasgado_transparente.png"

    with open(srt_path, encoding='utf-8') as f:
        conteudo = f.read().strip().split("\n\n")

    for i, bloco in enumerate(conteudo):
        linhas = bloco.strip().split("\n")
        if len(linhas) < 3:
            continue

        tempo = linhas[1]
        texto = linhas[2]
        try:
            # Calcula tempos
            inicio_str, _ = tempo.split(" --> ")
            h, m, s_ms = inicio_str.split(":")
            s, ms = s_ms.split(',')

            inicio = int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000
            fim = inicio + 13
            if fim > video.duration:
                fim = video.duration

            trecho = video.subclip(inicio, fim).resize((largura, altura))

            # Cria legenda (TextClip)
            texto_legenda = TextClip(
                txt=texto,
                fontsize=24,
                font=fonte,
                color='yellow',
                method='caption',
                size=(int(largura * 0.6), None),  # largura menor, igual ao banner
                align='center',
                stroke_color='black',
                stroke_width=1
            ).set_duration(trecho.duration)

            # Calcula altura da legenda
            altura_legenda = texto_legenda.h

            # Carrega banner com transparência (tamanho menor)
            banner = (ImageClip(banner_transparente)
                      .resize(width=int(largura * 0.6))  # reduzido para 60% da largura
                      .set_duration(trecho.duration))

            # Calcula altura do banner
            altura_banner = banner.h

            # Posição vertical do topo do banner: mais perto da base (30px acima)
            pos_y_banner = altura - altura_banner - (-125)

            # Centraliza legenda verticalmente dentro do banner
            legenda_pos_y = pos_y_banner + (altura_banner - altura_legenda) / 2

            # Aplica posições
            banner = banner.set_position(("center", pos_y_banner))
            legenda = texto_legenda.set_position(("center", legenda_pos_y)).fx(fadein, 0.5)

            # Composição final
            final = CompositeVideoClip(
                [trecho, banner, legenda],
                size=(largura, altura)
            )

            # Salva arquivo
            nome_arquivo = os.path.join(pasta_saida, f"reel_{i+1:02}.mp4")

            final.write_videofile(
                nome_arquivo,
                codec="libx264",
                audio_codec="aac",
                preset="fast",
                threads=4,
                fps=30,
                ffmpeg_params=["-movflags", "+faststart"]
            )

        except Exception as e:
            print(f"❌ Erro no bloco {i+1}: {e}")

    print("✅ Todos os Reels foram gerados com sucesso!")

if __name__ == "__main__":
    video = r"D:\Fabrica de cortes\G4\alfredo\como_montar_times.mp4"
    srt = r"D:\Fabrica de cortes\G4\alfredo\legenda_combinada_para_reels.srt"
    saida = r"D:\Fabrica de cortes\G4\alfredo\reels2"
    gerar_reels(video, srt, saida)