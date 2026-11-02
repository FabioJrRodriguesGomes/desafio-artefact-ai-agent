
import csv
import os
from pathlib import Path

# Localiza os arquivos CSV na mesma pasta deste script
pasta = Path(__file__).parent
arquivos = sorted(pasta.glob("*.csv"))

if not arquivos:
    print("ERRO: Nenhum arquivo CSV encontrado!")
    print("Coloque os arquivos CSV na mesma pasta deste script.")

for arquivo in arquivos:
    print("\n" + "=" * 60)
    print(f"ARQUIVO: {arquivo.name}")
    print("=" * 60)

    try:
        # Tenta abrir com UTF-8
        try:
            f = open(arquivo, "r", encoding="utf-8-sig", newline="")
            f.read(1000)
            f.seek(0)
        except UnicodeDecodeError:
            f = open(arquivo, "r", encoding="latin-1", newline="")

        with f:
            amostra = f.read(4096)
            f.seek(0)

            # Identifica automaticamente o separador
            try:
                separador = csv.Sniffer().sniff(
                    amostra, delimiters=",;|\t"
                ).delimiter
            except csv.Error:
                separador = ","

            leitor = csv.DictReader(f, delimiter=separador)
            colunas = leitor.fieldnames or []
            registros = list(leitor)

            print("\nCOLUNAS:")
            print(colunas)

            print("\nQUANTIDADE DE REGISTROS:")
            print(len(registros))

            print("\nPRIMEIRAS 3 LINHAS:")
            for linha in registros[:3]:
                print(linha)

    except Exception as erro:
        print(f"ERRO AO LER ARQUIVO: {erro}")

print("\n" + "=" * 60)
print("ANÁLISE FINALIZADA!")
print("=" * 60)