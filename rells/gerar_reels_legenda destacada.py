from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ImageClip, ColorClip
from moviepy.config import change_settings
from moviepy.video.fx.fadein import fadein
from PIL import Image
import os

# Compatibilidade Pillow
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

# Caminho do ImageMagick
change_settings({
    "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
})

def gerar_reels(video_path, srt_path, pasta_saida, largura=960, altura=540, fonte='Arial-Bold', fontsize=40):
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    video = VideoFileClip(video_path)

    with open(srt_path, encoding='utf-8') as f:
        conteudo = f.read().strip().split("\n\n")

    for i, bloco in enumerate(conteudo):
        linhas = bloco.strip().split("\n")
        if len(linhas) < 3:
            continue

        tempo = linhas[1]
        texto = linhas[2]
        try:
            inicio_str, _ = tempo.split(" --> ")
            h, m, s_ms = inicio_str.split(":")
            s, ms = s_ms.split(',')

            inicio = int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
            fim = inicio + 10
            if fim > video.duration:
                fim = video.duration

            trecho = video.subclip(inicio, fim).resize((largura, altura))

            # Cria o TextClip da legenda
            texto_legenda = TextClip(
                txt=texto,
                fontsize=fontsize,
                font=fonte,
                color='yellow',
                method='caption',
                size=(int(largura * 0.9), None),
                align='center'
            ).set_duration(trecho.duration)

            # Dimensões do banner vermelho
            altura_banner = texto_legenda.h + 30
            pos_y_banner = altura - altura_banner

            # Cria o banner vermelho e posiciona abaixo
            banner = (ImageClip(r"D:\Fabrica de cortes\G4\alfredo\banner_rasgado.png")
                      .resize(width=largura)  # ajuste largura
                      .set_duration(trecho.duration)
                      .set_position(("center", altura - 100)))  # ajusta verticalmente

            # Posiciona o texto centralizado dentro do banner
            legenda_pos_y = pos_y_banner + (altura_banner - texto_legenda.h) // 2
            legenda = texto_legenda.set_position(("center", legenda_pos_y)).fx(fadein, 0.5)

            # Marca d’água no centro
            marca_dagua = (ImageClip(r"D:\Fabrica de cortes\G4\alfredo\_ulfrlobo__1_-removebg-preview.png")
                           .resize(height=60)
                           .set_duration(trecho.duration)
                           .set_position('center')
                           .set_opacity(0.6))

            # Composição final
            final = CompositeVideoClip(
                [trecho, banner, legenda, marca_dagua],
                size=(largura, altura)
            )

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
