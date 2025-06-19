from PIL import Image

def tornar_fundo_transparente(caminho_entrada, caminho_saida):
    img = Image.open(caminho_entrada).convert("RGBA")
    datas = img.getdata()

    nova_data = []
    for item in datas:
        # transforma pixels brancos (ou quase brancos) em transparente
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            # pixel branco vira transparente
            nova_data.append((255, 255, 255, 0))
        else:
            nova_data.append(item)

    img.putdata(nova_data)
    img.save(caminho_saida, "PNG")

if __name__ == "__main__":
    caminho_entrada = r"D:\Fabrica de cortes\G4\alfredo\banner_rasgado.png"
    caminho_saida = r"D:\Fabrica de cortes\G4\alfredo\banner_rasgado_transparente.png"
    tornar_fundo_transparente(caminho_entrada, caminho_saida)
    print("Fundo branco removido com sucesso e imagem salva em:", caminho_saida)
