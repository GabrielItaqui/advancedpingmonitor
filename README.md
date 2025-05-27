Monitor de Ping Avançado

Este repositório contém um script Python simples e eficaz para monitorar a disponibilidade de um host (IP ou nome de domínio) ao longo do tempo, registrando o status em um arquivo de log e gerando um relatório detalhado de disponibilidade.
Como Usar
Pré-requisitos

Certifique-se de ter o Python 3 instalado em seu sistema.
Instalação

Não há pacotes externos para instalar. Basta baixar o arquivo ping_monitor.py (ou o nome que você salvou o código) para o seu computador.
Execução

Para executar o script, abra um terminal ou prompt de comando, navegue até o diretório onde salvou o arquivo e execute o seguinte comando:
Bash

python ping_monitor.py

O script o guiará através de algumas perguntas de configuração:

    IP ou Host de Destino: O endereço IP (ex: 8.8.8.8) ou nome de domínio (ex: google.com) que você deseja monitorar.
    Tempo entre Pings (Intervalo): O tempo, em segundos, que o script aguardará entre uma verificação de ping e outra (ex: 60 para verificar a cada minuto).
    Latência do Ping (Timeout): O tempo, em segundos, que o script esperará por uma resposta do ping antes de considerar o host offline (ex: 1 para esperar 1 segundo).
    Tamanho do Pacote de Ping (Payload Size): O tamanho, em bytes, do pacote de dados ICMP a ser enviado. Valores comuns incluem 32, 64 ou 1500 (MTU máximo). Um valor de 0 pode ser usado para que o sistema operacional utilize um tamanho padrão.

Parando o Monitoramento e Gerando o Relatório

O monitoramento continuará indefinidamente até que você o pare. Para parar o monitoramento a qualquer momento e gerar o relatório, basta pressionar Ctrl + C no terminal onde o script está sendo executado.

Ao ser interrompido, o script automaticamente processará o arquivo de log e gerará um relatório sumário.
Arquivos Gerados

Após a execução, o script criará dois arquivos no mesmo diretório:

    Arquivo de Log (ping_log_*.txt): Contém um registro cronológico de cada verificação de ping, indicando se o host estava ONLINE ou OFFLINE em determinado timestamp. O nome do arquivo incluirá o host monitorado e a data/hora de início do monitoramento (ex: ping_log_google_com_20231027_103000.txt).
    Arquivo de Relatório (ping_report_*.txt): Um sumário da disponibilidade do host, incluindo a porcentagem geral de tempo online e uma lista de todos os períodos de inatividade detectados, com seus horários de início, fim e duração. O nome do arquivo seguirá o mesmo padrão do log (ex: ping_report_google_com_20231027_103000.txt).

Potenciais Utilidades

Este script, embora simples, oferece diversas utilidades práticas para monitoramento básico de rede:

    Monitoramento de Conectividade com a Internet: Verifique a estabilidade da sua própria conexão de internet pingando um servidor DNS público (como 8.8.8.8) ou um site conhecido.
    Acompanhamento de Servidores e Aplicações: Monitore a disponibilidade de servidores web, bancos de dados ou outros serviços importantes em sua rede local ou em nuvem. Se um servidor ficar offline, o script registrará o evento, permitindo uma análise posterior.
    Diagnóstico de Problemas de Rede Intermitentes: Para problemas de conectividade que aparecem e desaparecem, o log detalhado pode ajudar a identificar os momentos exatos das falhas, facilitando a investigação da causa raiz.
    Validação de SLA (Service Level Agreement): Embora não seja uma ferramenta de nível empresarial, pode fornecer dados básicos para verificar se um provedor de serviços está cumprindo os acordos de nível de serviço de disponibilidade para um determinado host.
    Ferramenta Educacional: Excelente para estudantes e iniciantes em redes que desejam entender como o comando ping funciona, como registrar dados e como gerar relatórios simples.
    Alerta Básico (com Extensão): Embora o script atual apenas registre, ele pode ser facilmente estendido para enviar notificações (e-mail, SMS, mensagens para Discord/Telegram) quando um host ficar offline ou voltar a ficar online.
    Teste de Estabilidade de Rede Doméstica: Se você suspeita de problemas com seu roteador ou provedor, rodar este script em um dispositivo conectado à sua rede pode fornecer evidências claras de quedas de conectividade.
