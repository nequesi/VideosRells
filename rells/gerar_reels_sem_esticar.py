from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ImageClip, concatenate_videoclips
from moviepy.config import change_settings
from PIL import Image
import os

# Compatibilidade Pillow
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

# Caminho do ImageMagick
change_settings({
    "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
})

def gerar_reels(video_path, srt_path, pasta_saida, largura=540, altura=960, fonte='Arial-Bold', fontsize=40):
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

            # Redimensiona o vídeo para altura de 960, mantendo proporção
            trecho = video.subclip(inicio, fim).resize(height=altura)

            # Faz o crop horizontalmente para largura de 540, mantendo centro
            x_center = trecho.w / 2
            x1 = int(x_center - largura / 2)
            x2 = int(x_center + largura / 2)
            trecho = trecho.crop(x1=x1, y1=0, x2=x2, y2=altura)

            # Legenda posicionada dentro da área segura
            legenda = (TextClip(
                txt=texto,
                fontsize=fontsize,
                font=fonte,
                color='white',
                size=(int(largura * 0.9), None),
                method='caption',
                align='center'
            )
            .set_duration(trecho.duration)
            .set_position(('center', altura - 300)))

            # Marca d’água central
            marca_dagua = (ImageClip(r"D:\Fabrica de cortes\G4\alfredo\ulfrlobo.png")
                           .resize(height=60)
                           .set_duration(trecho.duration)
                           .set_position("center")
                           .set_opacity(0.6))

            video_base = CompositeVideoClip([trecho, legenda, marca_dagua], size=(largura, altura))

            mensagem_final = (TextClip(
                "Gostou? Então curte e compartilha! 💥",
                fontsize=50,
                font=fonte,
                color='white',
                size=(largura, altura),
                method='caption',
                align='center'
            )
            .set_duration(3)
            .set_position('center'))

            video_completo = concatenate_videoclips([video_base, mensagem_final])

            nome_arquivo = os.path.join(pasta_saida, f"reel_{i+1:02}.mp4")

            video_completo.write_videofile(
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

    # Libera os arquivos de vídeo
    video.reader.close()
    if video.audio:
        video.audio.reader.close_proc()

    print("✅ Todos os Reels foram gerados com sucesso!")

if __name__ == "__main__":
    video = r"D:\Fabrica de cortes\G4\alfredo\como_montar_times.mp4"
    srt = r"D:\Fabrica de cortes\G4\alfredo\legenda_combinada_para_reels.srt"
    saida = r"D:\Fabrica de cortes\G4\alfredo\reels_crop"
    gerar_reels(video, srt, saida)
