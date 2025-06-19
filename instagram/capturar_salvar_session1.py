from instagrapi import Client
import json

SESSION_FILE = r"D:\MeusDadosSeguros\instagram_session.json"

def salvar_sessionid():
    cl = Client()
    username = input("👤 Usuário: ")
    password = input("🔑 Senha: ")
    username = "ulfrlobo@gmail.com"
    password = "Lobo&ulfr"
    cl.login(username, password)

    with open(SESSION_FILE, "w") as f:
        json.dump({"sessionid": cl.sessionid}, f)
    print("✅ sessionid salvo com sucesso.")

def main():
    salvar_sessionid()
username = 'ulfrlobo@gmail.com'
password = 'Lobo&ulfr'
if __name__ == "__main__":
    main()

