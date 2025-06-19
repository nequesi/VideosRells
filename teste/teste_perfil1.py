import undetected_chromedriver as uc
import json
import os
import time

COOKIES_FILE = r"D:\MeusDadosSeguros\cookies_instagram.json"

def iniciar_driver():
    options = uc.ChromeOptions()
    # Ex: options.add_argument("--headless")  # Opcional, se quiser oculto
    return uc.Chrome(options=options)

def salvar_cookies(driver):
    cookies = driver.get_cookies()
    with open(COOKIES_FILE, "w") as f:
        json.dump(cookies, f)
    print("✅ Cookies salvos.")

def carregar_cookies(driver):
    with open(COOKIES_FILE, "r") as f:
        cookies = json.load(f)
    for cookie in cookies:
        if "sameSite" in cookie:
            cookie["sameSite"] = "Strict"
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f"⚠️ Erro ao adicionar cookie: {e}")

def main():
    driver = iniciar_driver()
    driver.get("https://www.instagram.com")
    time.sleep(3)

    if os.path.exists(COOKIES_FILE):
        print("🔄 Carregando cookies existentes...")
        carregar_cookies(driver)
        driver.get("https://www.instagram.com")  # Recarrega com cookies
    else:
        print("🔐 Faça o login manual (incluindo 2FA) e pressione Enter...")
        input("▶️ Após login completo, pressione Enter para continuar...")
        salvar_cookies(driver)

    print("✅ Pronto! Login realizado.")
    input("🔒 Pressione Enter para fechar o navegador...")
    driver.quit()

if __name__ == "__main__":
    main()




