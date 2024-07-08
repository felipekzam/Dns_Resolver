import socket
import argparse
import signal
import time

def color_print(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")

def is_valid_domain(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

def is_valid_wordlist(wordlist_file):
    try:
        with open(wordlist_file, "r") as file:
            return len(file.readlines()) > 0
    except FileNotFoundError:
        return False

def resolve_subdomains(domain, wordlist):
    total = len(wordlist)
    count = 0
    start_time = time.time()  # Iniciar o cronômetro
    for subdomain in wordlist:
        subdomain = subdomain.rstrip(".")
        try:
            full_domain = f"{subdomain}.{domain}"
            encoded_domain = full_domain.encode("idna").decode("ascii")
            ip_address = socket.gethostbyname(encoded_domain)
            color_print(f"{full_domain} -> {ip_address}", "32")
        except (socket.gaierror, UnicodeError):
            pass
        count += 1
        print(f"Progresso: {count}/{total} ({(count/total)*100:.1f}%)", end="\r")
    print("\n")
    end_time = time.time()
    execution_time = end_time - start_time
    color_print(f"\nTempo de execução: {execution_time:.2f} segundos", "36")  # Ciano

def signal_handler(sig, frame):
    color_print("\n\nPrograma interrompido pelo usuário (Ctrl+C).", "31")
    exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)

    color_print("\n\nBem-vindo ao Resolvedor de DNS!", "32")
    print("\n")
    color_print("Instruções:", "33")
    print("\n")
    print("1. Digite o domínio alvo (ex: exemplo.com)")
    print("2. Digite o caminho para o arquivo de wordlist (ex: wordlist.txt)")
    print("3. Pressione Ctrl+C para encerrar o programa\n")

    while True:
        while True:
            domain = input("\nDomínio alvo: ")
            if domain.lower() == "sair":
                color_print("\nEncerrando o programa...", "31")
                exit(0)
            if is_valid_domain(domain):
                domain = domain.replace("www.", "")
                break
            else:
                color_print("\nDomínio inválido. Digite um domínio válido.", "31")

        while True:
            wordlist_file = input("\nCaminho para o arquivo de wordlist: ")
            if wordlist_file.lower() == "sair":
                color_print("\nEncerrando o programa...", "31")
                exit(0)
            if is_valid_wordlist(wordlist_file):
                with open(wordlist_file, "r") as file:
                    wordlist = [line.strip() for line in file]
                break
            else:
                color_print("\nWordlist inválida ou não encontrada. Digite um caminho válido.", "31")

        resolve_subdomains(domain, wordlist)

        while True:
            continuar = input("\nDeseja fazer outra consulta? (s/n): ")
            if continuar.lower() in ["s", "n"]:
                break
            else:
                color_print("\nOpção inválida. Digite 's' para sim ou 'n' para não.", "31")

        if continuar.lower() == "n":
            color_print("\nEncerrando o programa...", "31")
            break

if __name__ == "__main__":
    main()
