import os
import time
import shutil
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import random

def get_user_input():
    print(">>> Iniciando entrada de dados...")
    videos_folder_input = 'D:/teste_instagram'
    # videos_folder_input = input("Digite o caminho completo da pasta de vídeos: ")
    video_limit = 2
    # video_limit = int(input("Quantos vídeos deseja postar por vez? "))
    wait_minutes = 3
    # wait_minutes = int(input("Tempo de espera entre postagens (em minutos): "))
    caption_input = "pinga fogo, professor, aula"
    # caption_input = input("Digite as hashtags/legendas separadas por vírgula: ")

    captions = [c.strip() for c in caption_input.split(",") if c.strip()]
    videos_folder = Path(videos_folder_input).expanduser().resolve()

    if not videos_folder.exists() or not videos_folder.is_dir():
        print(f"Erro: A pasta '{videos_folder}' não existe ou não é uma pasta válida.")
        exit(1)

    return videos_folder, video_limit, wait_minutes, captions

def setup_browser_with_profile():
    options = Options()
    # Altere esse caminho para o caminho correto do seu perfil do Chrome
    # options.add_argument(r'--user-data-dir=C:\Users\walhe\AppData\Local\Google\Chrome\User Data')
    # options.add_argument('--profile-directory=Profile 1')
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

def aguardar_login(driver):
    driver.get("https://www.instagram.com/")
    input(">>> Faça login manualmente e pressione Enter para continuar...")

def post_video(driver, video_path, caption):
    try:
        driver.get("https://www.instagram.com/")
        time.sleep(random.randint(3, 6))

        upload_btn = driver.find_element(By.XPATH, "//div[text()='Criar']/..")
        upload_btn.click()
        time.sleep(3)

        file_input = driver.find_element(By.XPATH, "//input[@accept='video/mp4,video/x-m4v,video/*']")
        file_input.send_keys(str(video_path))
        time.sleep(5)

        for _ in range(2):
            next_btn = driver.find_element(By.XPATH, "//div[text()='Avançar']")
            next_btn.click()
            time.sleep(3)

        caption_area = driver.find_element(By.XPATH, "//textarea[@aria-label='Escreva uma legenda...']")
        caption_area.send_keys(caption)
        time.sleep(2)

        share_btn = driver.find_element(By.XPATH, "//div[text()='Compartilhar']")
        share_btn.click()
        time.sleep(10)

        return True
    except Exception as e:
        print(f"Erro ao postar vídeo {video_path.name}: {e}")
        return False

def post_videos(driver, videos_folder, video_limit, captions):
    posted_folder = videos_folder / "posted"
    posted_folder.mkdir(exist_ok=True)

    videos = list(videos_folder.glob("*.mp4"))[:video_limit]
    if not videos:
        print("Nenhum vídeo disponível para postar.")
        return False

    for video_path in videos:
        print(f"Postando vídeo: {video_path.name}")
        caption = random.choice(captions)
        if post_video(driver, video_path, caption):
            shutil.move(str(video_path), posted_folder / video_path.name)
        else:
            print(f"Falha ao postar: {video_path.name}")
    return True

def main():
    videos_folder, video_limit, wait_minutes, captions = get_user_input()
    driver = setup_browser_with_profile()
    aguardar_login(driver)

    while True:
        has_videos = post_videos(driver, videos_folder, video_limit, captions)
        if not has_videos:
            print("Todos os vídeos foram postados.")
            break
        print(f"Aguardando {wait_minutes} minutos para próxima postagem...")
        time.sleep(wait_minutes * 60)

    driver.quit()

if __name__ == "__main__":
    main()
