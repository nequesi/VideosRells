import re

def srt_time_to_seconds(srt_time):
    h, m, s_ms = srt_time.split(':')
    s, ms = s_ms.split(',')
    return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000

def seconds_to_srt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def combinar_legenda(path_entrada, path_saida, alvo=10, minimo=8, maximo=12, limite_blocos=70):
    with open(path_entrada, "r", encoding="utf-8") as f:
        conteudo = f.read()

    blocos = conteudo.strip().split("\n\n")
    combinados = []
    buffer = []
    buffer_inicio = None
    buffer_fim = None
    duracao_total = 0

    for bloco in blocos:
        linhas = bloco.strip().split("\n")
        if len(linhas) < 3:
            continue

        try:
            tempos = linhas[1]
            inicio_str, fim_str = tempos.split(" --> ")
            inicio = srt_time_to_seconds(inicio_str)
            fim = srt_time_to_seconds(fim_str)
            duracao = fim - inicio
            texto = " ".join(linhas[2:]).strip()

            if not buffer:
                buffer_inicio = inicio
                buffer_fim = fim
                duracao_total = duracao
                buffer = [texto]
            else:
                duracao_total += duracao
                buffer_fim = fim
                buffer.append(texto)

            if duracao_total >= minimo:
                if duracao_total <= maximo:
                    combinados.append({
                        "inicio": seconds_to_srt_time(buffer_inicio),
                        "fim": seconds_to_srt_time(buffer_fim),
                        "texto": " ".join(buffer)
                    })
                    buffer = []
                    duracao_total = 0

            if len(combinados) >= limite_blocos:
                break

        except Exception as e:
            continue

    # Salva novo .srt
    with open(path_saida, "w", encoding="utf-8") as f:
        for i, bloco in enumerate(combinados, start=1):
            f.write(f"{i}\n")
            f.write(f"{bloco['inicio']} --> {bloco['fim']}\n")
            f.write(f"{bloco['texto']}\n\n")

    print(f"✅ {len(combinados)} blocos combinados salvos em: {path_saida}")

# 🏃 Rodar
if __name__ == "__main__":
    entrada = r"D:\Fabrica de cortes\G4\alfredo\portugues_asr.srt"
    saida = r"D:\Fabrica de cortes\G4\alfredo\legenda_combinada_para_reels.srt"
    combinar_legenda(entrada, saida)
