from moviepy.editor import VideoFileClip, clips_array, concatenate_videoclips
from moviepy.config import change_settings
from PIL import Image

# Compatibilidade com Pillow >= 10.0
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

# Configura o caminho para o ImageMagick
change_settings({
    "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
})

def criar_video_com_split_vertical():
    # Caminho base dos arquivos
    caminho = r"D:\Fabrica de cortes\G4"

    # Carrega os vídeos
    especialista = VideoFileClip(f"{caminho}\\especialista.mp4")
    satisfatorio = VideoFileClip(f"{caminho}\\satisfatorio.mp4")

    # Define o formato de saída: escolha 1 opção descomentando abaixo
    # 🔵 Opção 1: Landscape (padrão) 1280x720
    output_width = 1280
    output_height = 720

    # 🔵 Opção 2: Vertical (celular) 720x1280
    # output_width = 720
    # output_height = 1280

    # 🔵 Opção 3: Quadrado 720x720
    # output_width = 720
    # output_height = 720

    # Altura de cada vídeo na divisão (metade da altura total)
    video_height = output_height // 2

    # Redimensiona e corta os vídeos para preencher exatamente a área
    especialista_resized = especialista.resize(newsize=(output_width, video_height)).crop(x1=0, y1=0, x2=output_width, y2=video_height)
    satisfatorio_resized = satisfatorio.resize(newsize=(output_width, video_height)).crop(x1=0, y1=0, x2=output_width, y2=video_height)

    # Repete satisfatório até completar a duração do especialista
    duracao_esp = especialista_resized.duration
    repeticoes = int(duracao_esp // satisfatorio_resized.duration) + 1
    satisfatorio_loop = concatenate_videoclips([satisfatorio_resized] * repeticoes).subclip(0, duracao_esp)

    # Junta os vídeos (especialista em cima, satisfatório embaixo)
    video_final = clips_array([[especialista_resized],
                               [satisfatorio_loop]])

    # Exporta com o nome correspondente
    saida = f"{caminho}\\video_final_split.mp4"
    video_final.write_videofile(saida, codec="libx264", audio_codec="aac")

if __name__ == "__main__":
    criar_video_com_split_vertical()
