# postar_reels_com_delays.py
import os
import time
import shutil
import random
import json
from instagrapi import Client
from pathlib import Path

SESSION_FILE = r"D:\MeusDadosSeguros\instagram_session.json"

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

def post_reels(cl, videos_folder, legenda):
    posted_folder = videos_folder / "posted"
    if not posted_folder.exists():
        posted_folder.mkdir(parents=True)

    videos = list(videos_folder.glob("*.mp4"))

    if not videos:
        print("Nenhum vídeo encontrado para postar.")
        return

    videos = videos[:10]  # Limita a até 10 vídeos

    for video_path in videos:
        esperar_aleatorio(1.5, 4, "antes de iniciar o upload")

        print(f"🎥 Postando como Reels: {video_path.name}")
        try:
            cl.clip_upload(
                path=str(video_path),
                caption=legenda
            )
            esperar_aleatorio(2, 5, "após upload")

            mover_com_espera(str(video_path), str(posted_folder / video_path.name))
            print("✅ Postado com sucesso.")

            esperar_aleatorio(1, 3, "antes do próximo vídeo")

        except Exception as e:
            print(f"❌ Erro ao postar {video_path.name}: {e}")
            esperar_aleatorio(5, 10, "após erro")

def main():
    videos_folder_input = "D:\post_video_instagram"
    videos_folder = Path(videos_folder_input).expanduser().resolve()

    if not videos_folder.exists() or not videos_folder.is_dir():
        print(f"Erro: A pasta '{videos_folder}' não é válida.")
        return

    legenda = " #professorPingaFogo"

    cl = Client()
    cl.set_user_agent("Instagram 250.0.0.17.115 Android")
    carregar_sessionid(cl)

    while True:
        post_reels(cl, videos_folder, legenda)
        delay = random.randint(60, 180)  # 1 a 3 minutos
        print(f"⏳ Aguardando {delay // 60} minutos para a próxima rodada...")
        time.sleep(delay)

if __name__ == "__main__":
    main()


