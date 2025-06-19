# postar_reels_com_delays.py
import os
import time
import shutil
import random
import json
from instagrapi import Client
from pathlib import Path

SESSION_FILE = r"D:\MeusDadosSeguros\instagram_session.json"
MAX_POR_HORA = 3  # Limita a 3 vídeos por hora

def esperar_aleatorio(min_seg=2, max_seg=5, contexto=""):
    tempo = random.uniform(min_seg, max_seg)
    if contexto:
        print(f"🕒 Aguardando {tempo:.1f}s ({contexto})...")
    time.sleep(tempo)

def carregar_sessionid(cl):
    if not os.path.exists(SESSION_FILE):
        print("❌ sessionid não encontrado. Execute o script de login primeiro.")
        exit(1)

    with open(SESSION_FILE, "r") as f:
        session_data = json.load(f)
    cl.login_by_sessionid(session_data["sessionid"])
    print("✅ Login com sessionid bem-sucedido.")

def mover_com_espera(origem, destino, tentativas=10, espera_seg=3):
    for i in range(tentativas):
        try:
            shutil.move(origem, destino)
            return True
        except PermissionError:
            print(f"⚠️ Arquivo ainda em uso ({i+1}/{tentativas}). Tentando novamente em {espera_seg}s...")
            time.sleep(espera_seg)
    print(f"❌ Falha ao mover o arquivo após {tentativas} tentativas.")
    return False

def post_reels(cl, videos_folder, legenda, max_videos=MAX_POR_HORA):
    posted_folder = videos_folder / "posted"
    posted_folder.mkdir(parents=True, exist_ok=True)

    todos_videos = list(videos_folder.glob("*.mp4"))
    videos = [v for v in todos_videos if not (posted_folder / v.name).exists()]

    if not videos:
        print("📭 Nenhum novo vídeo encontrado para postar.")
        return

    for idx, video_path in enumerate(videos[:max_videos]):
        esperar_aleatorio(1.5, 4, "antes de iniciar o upload")
        print(f"🎥 Postando como Reels: {video_path.name}")
        try:
            cl.clip_upload(
                path=str(video_path),
                caption=legenda
            )
            esperar_aleatorio(2, 5, "após upload")

            if mover_com_espera(str(video_path), str(posted_folder / video_path.name)):
                print("✅ Postado com sucesso.")

            esperar_aleatorio(10, 30, "antes do próximo vídeo")

        except Exception as e:
            print(f"❌ Erro ao postar {video_path.name}: {e}")
            esperar_aleatorio(30, 60, "após erro")

def main():
    videos_folder = Path(r"D:\post_video_instagram").expanduser().resolve()
    if not videos_folder.exists() or not videos_folder.is_dir():
        print(f"Erro: A pasta '{videos_folder}' não é válida.")
        return

    legenda = "#professorPingaFogo"
    cl = Client()
    cl.set_user_agent("Instagram 250.0.0.17.115 Android")
    carregar_sessionid(cl)

    while True:
        post_reels(cl, videos_folder, legenda)

        delay_minutos = random.randint(2, 4)  # Pausa de 20 a 40 minutos
        print(f"⏳ Aguardando {delay_minutos} minutos para a próxima rodada...")
        time.sleep(delay_minutos * 60)

if __name__ == "__main__":
    main()
