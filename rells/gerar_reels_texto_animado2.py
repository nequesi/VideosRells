from moviepy.editor import (
    VideoFileClip, TextClip, CompositeVideoClip, ImageClip, VideoClip
)
from moviepy.config import change_settings
from moviepy.video.fx.fadein import fadein
from PIL import Image
import os
import re

# Compatibilidade com Pillow
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

# Caminho do ImageMagick (confira se está correto)
change_settings({
    "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
})

def sanitize_text(text):
    # Remove quebras de linha, múltiplos espaços, e caracteres não imprimíveis
    text = re.sub(r'\s+', ' ', text)
    # Remove caracteres estranhos (pode ajustar conforme necessidade)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text.strip()

def efeito_digitando_continuo(texto, fonte, fontsize, cor, duracao):
    n_chars = len(texto)

    def make_frame(t):
        n = int(n_chars * (t / duracao))
        if n > n_chars:
            n = n_chars
        texto_parcial = texto[:n] if n > 0 else " "
        clip = TextClip(
            texto_parcial,
            # texto_parcial,
            fontsize=fontsize,
            font=fonte,
            color=cor,
            # stroke_color='red',
            # stroke_width=2,
            method='label',      # MELHOR para fundo transparente
            transparent=True     # Fundo transparente
        )
        return clip.img

    anim = VideoClip(make_frame, duration=duracao)
    return anim


def gerar_reels(video_path, srt_path, pasta_saida, largura=960, altura=540, fonte='Arial-Bold'):
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    video = VideoFileClip(video_path)
    banner_transparente = r"D:\Fabrica de cortes\G4\alfredo\banner_rasgado_transparente.png"
    marca_dagua_path = r"D:\Fabrica de cortes\G4\alfredo\ulfrlobo.png"

    with open(srt_path, encoding='utf-8') as f:
        conteudo = f.read().strip().split("\n\n")

    for i, bloco in enumerate(conteudo):
        linhas = bloco.strip().split("\n")
        if len(linhas) < 3:
            continue

        tempo = linhas[1]
        texto = linhas[2]
        try:
            # Extrai tempos
            inicio_str, _ = tempo.split(" --> ")
            h, m, s_ms = inicio_str.split(":")
            s, ms = s_ms.split(',')

            inicio = int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000
            fim = inicio + 13
            if fim > video.duration:
                fim = video.duration

            trecho = video.subclip(inicio, fim).resize((largura, altura))

            texto_sanitizado = sanitize_text(texto)

            # Texto da legenda tradicional
            texto_legenda = TextClip(
                txt=texto_sanitizado,
                fontsize=24,
                font=fonte,
                color='yellow',
                method='caption',
                size=(int(largura * 0.6), None),
                align='center',
                stroke_color='black',
                stroke_width=1
            ).set_duration(trecho.duration)

            altura_legenda = texto_legenda.h

            banner = (ImageClip(banner_transparente)
                      .resize(width=int(largura * 0.6))
                      .set_duration(trecho.duration))

            altura_banner = banner.h
            pos_y_banner = altura - altura_banner - (-125)
            legenda_pos_y = pos_y_banner + (altura_banner - altura_legenda) / 2

            banner = banner.set_position(("center", pos_y_banner))
            legenda = texto_legenda.set_position(("center", legenda_pos_y)).fx(fadein, 0.5)

            marca_dagua = (ImageClip(marca_dagua_path)
                           .resize(height=60)
                           .set_duration(trecho.duration)
                           .set_position('center')
                           .set_opacity(0.6))

            # Mensagem final (aparece nos últimos 2 segundos)
            dur_final = 2
            mensagem_final = (TextClip(
                "Gostou? Então curte e compartilha! 💥",
                fontsize=28,
                font=fonte,
                color='white',
                method='caption',
                size=(int(largura * 0.6), None),
                align='center'
            )
            .set_duration(dur_final)
            .set_position(("center", legenda_pos_y))
            .crossfadein(0.3)
            .set_start(trecho.duration - dur_final))

            # Pega a primeira frase curta para efeito digitando
            frases = texto_sanitizado.split('. ')
            frase_curta = frases[0] if frases else texto_sanitizado

            digitando_clip = efeito_digitando_continuo(
                frase_curta,
                fonte="Times-New-Roman",  # ou "Georgia", "Merriweather" etc
                fontsize=38,
                cor='yellow',
                duracao=3
            ).set_start(0).set_duration(3).set_position(("center", altura * 0.25))

            # Composição final incluindo o texto animado digitando
            final = CompositeVideoClip(
                [trecho, banner, digitando_clip, legenda, marca_dagua, mensagem_final],
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
    video = r"D:\Fabrica de cortes\brasil_paralelo\video.mp4"
    srt = r"D:\Fabrica de cortes\brasil_paralelo\legenda_combinada_para_reels.srt"
    saida = (r"D:\Fabrica de cortes\brasil_paralelo\reels_final2"
             r"")
    gerar_reels(video, srt, saida)
