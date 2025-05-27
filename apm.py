import subprocess
import datetime
import time
import os
import sys
import socket

# --- Variáveis Globais (serão definidas por input do usuário) ---
TARGET_HOST = ""
PING_INTERVAL_SECONDS = 0
PING_TIMEOUT_SECONDS = 0
PACKET_SIZE_BYTES = 0

# --- Variáveis de Nome de Arquivo (serão definidas dinamicamente) ---
LOG_FILE = ""
REPORT_FILE = ""

# --- Constantes para Mensagens (para melhor manutenção) ---
MSG_INVALID_NUMBER = "Entrada inválida. Por favor, digite um número inteiro."
MSG_POSITIVE_SECONDS = "O valor deve ser um número positivo de segundos."
MSG_NON_NEGATIVE_BYTES = "O tamanho não pode ser negativo."
MSG_HOST_EMPTY = "O IP/Host não pode ser vazio. Por favor, tente novamente."
MSG_HOST_RESOLUTION_FAILED = "Não foi possível resolver o host '{user_input}'. Por favor, verifique o nome ou o IP e tente novamente."
MSG_UNEXPECTED_HOST_ERROR = "Ocorreu um erro inesperado ao validar o host: {error}"


# --- Funções ---

def get_user_input():
    """
    Coleta todas as configurações do usuário: IP, intervalo, timeout e tamanho do pacote.
    """
    global TARGET_HOST, PING_INTERVAL_SECONDS, PING_TIMEOUT_SECONDS, PACKET_SIZE_BYTES

    print("--- Configuração do Monitoramento de Ping ---")

    # 1. IP de Destino
    while True:
        user_input_host = input("Digite o IP ou Host para monitorar (ex: 8.8.8.8 ou google.com): ").strip()
        if not user_input_host:
            print(MSG_HOST_EMPTY)
        else:
            try:
                # Tenta resolver o host para um IP. Isso valida se o host é acessível via DNS ou é um IP válido.
                resolved_ip = socket.gethostbyname(user_input_host)
                TARGET_HOST = user_input_host
                print(f"Host alvo definido: {TARGET_HOST} (IP resolvido: {resolved_ip})")
                break
            except socket.gaierror:
                print(MSG_HOST_RESOLUTION_FAILED.format(user_input=user_input_host))
            except Exception as e:
                print(MSG_UNEXPECTED_HOST_ERROR.format(error=e))

    # 2. Tempo entre Pings (Intervalo)
    while True:
        try:
            interval = int(input("Digite o tempo entre pings em segundos (ex: 60 para 1 minuto): ").strip())
            if interval <= 0:
                print(MSG_POSITIVE_SECONDS.replace("segundos", "segundos para o intervalo."))
            else:
                PING_INTERVAL_SECONDS = interval
                print(f"Intervalo de ping definido: {PING_INTERVAL_SECONDS} segundos.")
                break
        except ValueError:
            print(MSG_INVALID_NUMBER.replace("inteiro", "inteiro para o intervalo."))

    # 3. Latência do Ping (Timeout)
    while True:
        try:
            timeout = int(input("Digite a latência do ping em segundos (timeout de espera por resposta, ex: 1): ").strip())
            if timeout <= 0:
                print(MSG_POSITIVE_SECONDS.replace("segundos", "segundos para o timeout."))
            else:
                PING_TIMEOUT_SECONDS = timeout
                print(f"Timeout de ping definido: {PING_TIMEOUT_SECONDS} segundos.")
                break
        except ValueError:
            print(MSG_INVALID_NUMBER.replace("inteiro", "inteiro para o timeout."))

    # 4. Tamanho do Pacote (Payload Size)
    while True:
        try:
            packet_size = int(input("Digite o tamanho do pacote de ping em bytes (ex: 32, 64, 1500): ").strip())
            if packet_size < 0:
                print(MSG_NON_NEGATIVE_BYTES)
            elif packet_size == 0:
                 print("Considerando 0 bytes para o payload, o sistema pode usar um tamanho padrão.")
                 PACKET_SIZE_BYTES = packet_size
                 break
            else:
                PACKET_SIZE_BYTES = packet_size
                print(f"Tamanho do pacote de ping definido: {PACKET_SIZE_BYTES} bytes.")
                break
        except ValueError:
            print(MSG_INVALID_NUMBER.replace("inteiro", "inteiro para o tamanho do pacote."))

    # Define os nomes dos arquivos após todas as configurações estarem prontas
    start_time_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Substitui caracteres especiais no host para garantir um nome de arquivo válido
    safe_target_host = TARGET_HOST.replace('.', '_').replace(':', '_').replace('/', '_').replace('\\', '_')
    global LOG_FILE, REPORT_FILE
    LOG_FILE = f"ping_log_{safe_target_host}_{start_time_str}.txt"
    REPORT_FILE = f"ping_report_{safe_target_host}_{start_time_str}.txt"

    print(f"\nArquivos de log e relatório serão gerados com o prefixo '{start_time_str}'.")

def ping_host(host, timeout, packet_size):
    """
    Verifica a conectividade com o host usando o comando ping do sistema operacional.
    Retorna True se o ping for bem-sucedido, False caso contrário.
    """
    command = []
    try:
        if os.name == 'nt':  # Windows
            # -n 1: 1 pacote
            # -w <timeout_ms>: timeout em milissegundos
            # -l <size>: tamanho do buffer de envio
            command = ["ping", "-n", "1", "-w", str(timeout * 1000)]
            if packet_size > 0:
                command.extend(["-l", str(packet_size)])
            command.append(host)
        else:  # Linux/macOS (Unix-like)
            # -c 1: 1 pacote
            # -W <timeout_s>: timeout em segundos
            # -s <size>: tamanho do pacote de dados (excluindo o cabeçalho ICMP)
            command = ["ping", "-c", "1", "-W", str(timeout)]
            if packet_size > 0:
                command.extend(["-s", str(packet_size)])
            command.append(host)

        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout + 2) # Adiciona um buffer para o timeout do subprocess
        # O ping é bem-sucedido se o código de retorno for 0
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        # print(f"Erro: Timeout ao tentar pingar {host} com comando: {' '.join(command)}") # Para debug, pode ser útil
        return False
    except Exception as e:
        print(f"Ocorreu um erro ao executar o ping com comando {' '.join(command)}: {e}")
        return False

def log_status(status):
    """
    Registra o status de disponibilidade (online/offline) e o timestamp no arquivo de log.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_str = "ONLINE" if status else "OFFLINE"
    log_entry = f"{timestamp} - {status_str}\n" # Mantendo o '\n' para garantir que cada entrada ocupe uma nova linha

    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    print(f"Registrado: {log_entry.strip()}")

def generate_report():
    """
    Gera um relatório sumário a partir do arquivo de log.
    Calcula a porcentagem de tempo online e lista os períodos de inatividade.
    """
    online_count = 0
    offline_periods = []
    last_status = None
    last_timestamp = None
    total_checks = 0

    print(f"\nGerando relatório a partir de '{LOG_FILE}'...")

    try:
        with open(LOG_FILE, "r") as f:
            for line in f:
                total_checks += 1
                parts = line.strip().split(" - ")
                if len(parts) == 2:
                    timestamp_str, status_str = parts
                    current_timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    current_status = (status_str == "ONLINE")

                    if current_status:
                        online_count += 1
                    else:
                        # Detecta o início de um período offline
                        if last_status is None or last_status: # Se o status anterior era online ou é a primeira entrada
                            offline_periods.append({"start": current_timestamp, "end": None})

                    # Detecta o fim de um período offline
                    # Se o status anterior era offline e o atual é online, fecha o período
                    if last_status is False and current_status is True:
                        if offline_periods and offline_periods[-1]["end"] is None:
                            offline_periods[-1]["end"] = current_timestamp

                    last_status = current_status
                    last_timestamp = current_timestamp

            # Se o último status lido foi offline e o arquivo terminou, o período continua até agora
            if last_status is False and offline_periods and offline_periods[-1]["end"] is None:
                offline_periods[-1]["end"] = datetime.datetime.now() # Assume que o serviço está offline até o fim do monitoramento

    except FileNotFoundError:
        print(f"Arquivo de log '{LOG_FILE}' não encontrado. Nenhum relatório pode ser gerado.")
        return
    except Exception as e:
        print(f"Erro ao ler o arquivo de log: {e}")
        return

    report_content = []
    report_content.append(f"--- Relatório de Disponibilidade de {TARGET_HOST} ---\n")
    report_content.append(f"Configurações do Ping: Intervalo={PING_INTERVAL_SECONDS}s, Latência={PING_TIMEOUT_SECONDS}s, Tamanho do Pacote={PACKET_SIZE_BYTES} bytes\n")
    report_content.append(f"Período do Relatório: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_content.append(f"Número total de verificações: {total_checks}\n")

    if total_checks > 0:
        availability_percentage = (online_count / total_checks) * 100
        report_content.append(f"Disponibilidade Geral: {availability_percentage:.2f}%\n\n")
    else:
        report_content.append("Nenhuma verificação de ping registrada.\n\n")

    if offline_periods:
        report_content.append("Períodos de Inatividade Detectados:\n")
        for period in offline_periods:
            start_str = period["start"].strftime("%Y-%m-%d %H:%M:%S")
            end_str = period["end"].strftime("%Y-%m-%d %H:%M:%S") if period["end"] else "Ainda offline"
            duration = period["end"] - period["start"] if period["end"] else "N/A"
            report_content.append(f"- De: {start_str} Até: {end_str} (Duração: {duration})\n")
    else:
        report_content.append("Nenhum período de inatividade detectado.\n")

    with open(REPORT_FILE, "w") as f:
        f.writelines(report_content)
    print(f"Relatório gerado com sucesso em '{REPORT_FILE}'")
    print("".join(report_content)) # Imprime o relatório no console também

def main():
    """
    Função principal que agenda as verificações de ping e gera relatórios.
    """
    print("Bem-vindo ao Monitor de Ping Avançado!")
    print("Este programa irá rastrear a disponibilidade de um host e gerar um relatório detalhado.")
    print("Pressione Ctrl+C a qualquer momento para parar o monitoramento e gerar o relatório.\n")

    get_user_input() # Coleta todas as configurações do usuário

    print(f"\nIniciando o monitoramento de ping para {TARGET_HOST}...")
    print(f"Logs serão salvos em '{LOG_FILE}'")
    print(f"Relatórios serão salvos em '{REPORT_FILE}'\n")

    try:
        while True:
            is_online = ping_host(TARGET_HOST, PING_TIMEOUT_SECONDS, PACKET_SIZE_BYTES)
            log_status(is_online)
            time.sleep(PING_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\nMonitoramento interrompido pelo usuário.")
        generate_report()
        print("Saindo.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado na execução principal: {e}")
        sys.exit(1) # Sair com código de erro

# --- Execução ---
if __name__ == "__main__":
    main()
