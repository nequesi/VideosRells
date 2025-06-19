import os
import time
import shutil
import random
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass

def get_user_input():
    print(">>> Iniciando entrada de dados...")

    username = input("Digite seu usuário do Instagram: ")
    password = getpass.getpass("Digite sua senha do Instagram (não será exibida): ")
    videos_folder_input = 'D:/teste_instagram'
    # videos_folder_input = input("Digite o caminho completo da pasta de vídeos: ")
    # video_limit = int(input("Quantos vídeos deseja postar por vez? "))
    # wait_minutes = int(input("Tempo de espera entre postagens (em minutos): "))
    # caption_input = input("Digite as hashtags/legendas separadas por vírgula: ")
    video_limit = 2
    wait_minutes = 3
    caption_input = "pinga fogo, professor, aula"

    captions = [c.strip() for c in caption_input.split(",") if c.strip()]
    videos_folder = Path(videos_folder_input).expanduser().resolve()

    if not videos_folder.exists() or not videos_folder.is_dir():
        print(f"Erro: A pasta '{videos_folder}' não existe ou não é uma pasta válida.")
        exit(1)

    return username, password, videos_folder, video_limit, wait_minutes, captions

def setup_browser():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-popup-blocking")
    driver = webdriver.Chrome(options=options)
    return driver

def login(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    wait = WebDriverWait(driver, 15)

    try:
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

        print(">>> Aguardando autenticação (login)...")
        time.sleep(10)

        # Verifica se o código de verificação foi solicitado
        if "challenge" in driver.current_url or "checkpoint" in driver.current_url:
            print(">>> Código de verificação solicitado.")
            print(">>> Verifique seu e-mail e insira o código manualmente na tela do navegador.")
            input(">>> Pressione Enter aqui depois de inserir o código no navegador e confirmar...")

            # Aguarda redirecionamento para home
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//div[text()='Criar' or text()='Create']"))
            )
            print(">>> Autenticação 2FA concluída com sucesso.")
        else:
            print(">>> Login realizado sem autenticação adicional.")

    except Exception as e:
        print(f"[ERRO LOGIN] Falha ao fazer login: {e}")
        driver.quit()
        exit(1)

def post_video(driver, video_path, caption):
    try:
        print(f">>> Iniciando postagem do vídeo: {video_path.name}")
        driver.get("https://www.instagram.com/")
        time.sleep(random.randint(3, 6))

        # Botão de "Criar"
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Criar' or text()='Create']/.."))
        ).click()
        time.sleep(3)

        # Input de vídeo
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@accept='video/mp4,video/x-m4v,video/*']"))
        )
        file_input.send_keys(str(video_path))
        time.sleep(5)

        # Avançar (duas vezes)
        for _ in range(2):
            next_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='Avançar' or text()='Next']"))
            )
            next_btn.click()
            time.sleep(3)

        # Legenda
        caption_area = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[@aria-label='Escreva uma legenda...' or @aria-label='Write a caption…']"))
        )
        caption_area.send_keys(caption)
        time.sleep(2)

        # Compartilhar
        share_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Compartilhar' or text()='Share']"))
        )
        share_btn.click()
        time.sleep(10)

        print(f">>> Vídeo {video_path.name} postado com sucesso.")
        return True
    except Exception as e:
        print(f"[ERRO POSTAGEM] Falha ao postar vídeo {video_path.name}: {e}")
        return False

def post_videos(driver, videos_folder, video_limit, captions):
    posted_folder = videos_folder / "posted"
    posted_folder.mkdir(exist_ok=True)

    videos = list(videos_folder.glob("*.mp4"))[:video_limit]
    if not videos:
        print("Nenhum vídeo disponível para postar.")
        return False

    for video_path in videos:
        caption = random.choice(captions)
        success = post_video(driver, video_path, caption)
        if success:
            shutil.move(str(video_path), posted_folder / video_path.name)
        else:
            print(f"Falha ao postar: {video_path.name}")
    return True

def main():
    username, password, videos_folder, video_limit, wait_minutes, captions = get_user_input()
    driver = setup_browser()
    login(driver, username, password)

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
