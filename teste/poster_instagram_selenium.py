import os
import time
import shutil
import random
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import getpass
from selenium.webdriver.common.action_chains import ActionChains


def random_sleep(min_sec=2, max_sec=5):
    time.sleep(random.uniform(min_sec, max_sec))


def get_user_input():
    print(">>> Iniciando entrada de dados...")

    # username = input("👤 Usuário: ")
    # password = input("🔑 Senha: ")
    # username = input("Digite seu usuário do Instagram: ")
    # password = getpass.getpass("Digite sua senha do Instagram (não será exibida): ")
    username = "ulfrlobo@gmail.com"
    password = "Lobo&ulfr"
    videos_folder_input = 'D:/teste_instagram'
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
    # options.add_argument("--start-maximized")
    # options.add_argument("--disable-notifications")
    # options.add_argument("--disable-infobars")
    # options.add_argument("--disable-popup-blocking")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    # Caminho do perfil do Chrome para manter sessão já logada
    # Altere para o caminho do seu perfil de usuário no Chrome
    # options.add_argument(r"--user-data-dir=C:/Users/walhe/AppData/Local/Google/Chrome/User Data")
    # options.add_argument("--profile-directory=Profile 2")  # ou outro perfil que você usar
    options.add_argument(r"--user-data-dir=C:/Users/walhe/AppData/Local/Google/Chrome/User Data")
    options.add_argument(r"--profile-directory=Profile 2")

    # Caminho do chromedriver
    service = Service(r"C:/Users/walhe/Documents/dev_google/chromedriver-win64/chromedriver.exe")

    driver = webdriver.Chrome(service=service, options=options)
    return driver


def human_scroll(driver, amount=300):
    # Simula scroll suave para baixo
    driver.execute_script(f"window.scrollBy(0, {amount});")
    random_sleep(0.5, 1.5)


def login(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    wait = WebDriverWait(driver, 15)

    try:
        # Se o usuário já está logado, apenas retorna
        if "instagram.com" in driver.current_url and not "login" in driver.current_url:
            print(">>> Já logado no Instagram via perfil salvo.")
            return

        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

        print(">>> Aguardando autenticação (login)...")
        input(">>> Pressione Enter aqui para continuar após autenticar no navegador...")

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
        random_sleep(3, 6)

        human_scroll(driver, 400)

        # Botão de "Criar" (para novo post/reel)
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Criar' or text()='Create']/.."))
        ).click()
        random_sleep(3, 5)

        # Input de vídeo
        file_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@accept='video/mp4,video/x-m4v,video/*']"))
        )
        file_input.send_keys(str(video_path))
        random_sleep(6, 8)

        # Avançar (duas vezes)
        for _ in range(2):
            next_btn = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='Avançar' or text()='Next']"))
            )
            # Simula hover antes do clique
            ActionChains(driver).move_to_element(next_btn).perform()
            random_sleep(0.5, 1)
            next_btn.click()
            random_sleep(4, 6)

        # Legenda
        caption_area = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@aria-label='Escreva uma legenda...' or @aria-label='Write a caption…']"))
        )
        # Simula digitação lenta
        for char in caption:
            caption_area.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
        random_sleep(1, 2)

        # Compartilhar
        share_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Compartilhar' or text()='Share']"))
        )
        ActionChains(driver).move_to_element(share_btn).perform()
        random_sleep(0.5, 1)
        share_btn.click()
        random_sleep(10, 15)

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
