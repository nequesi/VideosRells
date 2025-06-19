# postar_videos.py
import os
import time
import shutil
import random
import json
from instagrapi import Client
from pathlib import Path

SESSION_FILE = "instagram_session.json"

def carregar_sessionid(cl):
    if not os.path.exists(SESSION_FILE):
        print("❌ sessionid não encontrado. Execute o script de login primeiro.")
        exit(1)

    with open(SESSION_FILE, "r") as f:
        session_data = json.load(f)
    cl.login_by_sessionid(session_data["sessionid"])
    print("✅ Login com sessionid bem-sucedido.")

def post_videos(cl, videos_folder):
    posted_folder = videos_folder / "posted"
    if not posted_folder.exists():
        posted_folder.mkdir(parents=True)

    videos = list(videos_folder.glob("*.mp4"))

    if not videos:
        print("Nenhum vídeo encontrado para postar.")
        return

    videos = videos[:10]  # Limita a até 10 vídeos

    for video_path in videos:
        print(f"🎥 Postando vídeo: {video_path.name}")
        try:
            cl.video_upload(str(video_path), caption="Seu texto aqui")
            shutil.move(str(video_path), posted_folder / video_path.name)
        except Exception as e:
            print(f"❌ Erro ao postar {video_path.name}: {e}")

def main():
    videos_folder_input = input("Digite o caminho completo da pasta de vídeos: ")
    videos_folder = Path(videos_folder_input).expanduser().resolve()

    if not videos_folder.exists() or not videos_folder.is_dir():
        print(f"Erro: A pasta '{videos_folder}' não é válida.")
        return

    cl = Client()
    carregar_sessionid(cl)

    while True:
        post_videos(cl, videos_folder)
        delay = random.randint(1, 3) * 60  # Espera entre 1 a 3 minutos
        print(f"⏳ Aguardando {delay // 60} minutos para a próxima postagem...")
        time.sleep(delay)

if __name__ == "__main__":
    main()
