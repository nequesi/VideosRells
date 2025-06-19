# salvar_sessionid.py
import undetected_chromedriver as uc
import json
import os
import time

SESSION_FILE = r"D:\MeusDadosSeguros\instagram_session.json"

def iniciar_driver():
    options = uc.ChromeOptions()
    return uc.Chrome(options=options)

def salvar_sessionid(driver):
    cookies = driver.get_cookies()
    for cookie in cookies:
        if cookie['name'] == 'sessionid':
            with open(SESSION_FILE, "w") as f:
                json.dump({"sessionid": cookie['value']}, f)
            print("✅ sessionid salvo com sucesso.")
            return
    print("❌ sessionid não encontrado. Faça login manualmente.")

def main():
    driver = iniciar_driver()
    driver.get("https://www.instagram.com")
    time.sleep(3)

    print("🔐 Faça login manualmente no Instagram (incluindo o código 2FA se necessário).")
    input("▶️ Após login completo, pressione Enter para capturar o sessionid...")

    salvar_sessionid(driver)

    input("🔒 Pressione Enter para fechar o navegador...")
    driver.quit()

if __name__ == "__main__":
    main()
