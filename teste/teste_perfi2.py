import undetected_chromedriver as uc

def main():
    user_data_dir = r"C:\Users\walhe\AppData\Local\Google\Chrome\User Data"
    profile_dir = "Profile 1"  # altere se seu perfil for outro, como "Default"

    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory={profile_dir}")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        driver = uc.Chrome(options=options)
        driver.get("https://www.instagram.com")
        print("Navegador aberto com seu perfil!")
    except Exception as e:
        print("❌ Erro ao iniciar o Chrome com Selenium:")
        print(e)

if __name__ == "__main__":
    main()

