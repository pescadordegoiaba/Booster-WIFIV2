# Booster-WIFIV2
    Importações de Bibliotecas:
    O script começa importando as bibliotecas necessárias, como subprocess para executar comandos do sistema, time para controle de tempo, numpy para operações numéricas, sklearn para criação de modelo de regressão linear, requests para fazer solicitações HTTP, BeautifulSoup para análise HTML, dns.resolver para resolução DNS e outras bibliotecas relacionadas.

    Funções para Medir Latência:
    Há uma função chamada measure_latency que utiliza o comando ping para medir a latência para um destino específico. Ela retorna uma lista de latências medidas.

    Classe CongestionModel:
    Essa classe encapsula o processo de treinamento de um modelo de regressão linear para avaliar o congestionamento da rede com base nas latências medidas.

    Função adjust_congestion_control:
    Essa função cria uma instância da classe CongestionModel e a treina com as latências fornecidas. Retorna o modelo treinado.

    Função set_tcp_window_scaling:
    Essa função ajusta o parâmetro de escalonamento de janela TCP.

    Função adjust_congestion_window:
    Esta função calcula e ajusta dinamicamente o tamanho da janela de congestionamento TCP com base nas latências observadas.

    Função set_dns_servers:
    Essa função substitui os servidores DNS nas configurações do sistema.

    Função optimize_dns:
    Essa função tenta otimizar as configurações de DNS, verificando a disponibilidade de servidores DNS personalizados.

    Funções para Aceleração de Conteúdo com CDN:
    As funções get_all_resources e accelerate_content_with_cdn coletam recursos de um endpoint, como imagens, e tentam acelerar o carregamento desses recursos utilizando uma CDN (Content Delivery Network).

    Função set_tcp_parameter:
    Essa função ajusta parâmetros TCP específicos do sistema.

    Função optimize_tcp_parameters:
    Essa função otimiza vários parâmetros do TCP/IP para melhorar o desempenho da rede.

    Função continuous_monitoring:
    Esta função seria implementada para monitorar a rede continuamente, mas a implementação real está faltando no exemplo.

    Funções para Gerenciamento de Potência Wi-Fi:
    Essas funções lidam com configurações de potência, gerenciamento de energia e modos de antena da interface Wi-Fi.

    Classe WiFiAP:
    Uma classe que modela um ponto de acesso Wi-Fi com nome e intensidade do sinal.

    Classe RoamingOptimizer:
    Essa classe simula o processo de roaming, onde um dispositivo muda para um ponto de acesso diferente quando detecta que o sinal do ponto atual é fraco.

    Classe WiFiChannel:
    Uma classe que modela um canal Wi-Fi com número de canal e nível de interferência.

    Classe ChannelOptimizer:
    Essa classe otimiza a seleção de canais Wi-Fi com base nos níveis de interferência.

    Classe AP:
    Modela um ponto de acesso Wi-Fi com nome e potência inicial.

    Classe PowerManager:
    Essa classe ajusta dinamicamente a potência de transmissão dos pontos de acesso com base na carga de rede.

    Classe QW:
    Modela uma qualidade de sinal Wi-Fi (Quality of Wireless) com nome e taxa de bits inicial.

    Classe BitrateManager:
    Essa classe ajusta a taxa de bits dinamicamente com base na qualidade do sinal e na taxa de perda de pacotes.

    Classe Fuel:
    Uma classe que modela pacotes com nome e prioridade.

    Classe PacketQueue:
    Essa classe implementa uma fila de pacotes com prioridades.

    Classe TrafficController:
    Essa classe adiciona pacotes à fila e processa pacotes com base nas prioridades.

    Execução Principal (if __name__ == "__main__":):
    Nesta seção, várias operações são realizadas sequencialmente, incluindo medição de latência, ajustes de configuração da interface Wi-Fi, cálculo do score de congestionamento, otimizações de DNS, aceleração de conteúdo com CDN, otimização de parâmetros TCP/IP, roaming, otimização de canais e processamento de pacotes.

    UPDATE 22/08/2023
    ADICIONEI UMA FUNÇÂO QUE REUTILIZA PACKETS PERDIDOS, ASSIM ENVIANDO OS PACKETS PERDIDOS NOVAMENTE, NÃO SEI SE AJUDA MAIS TA AI

Cabe ressaltar que este é um script bastante complexo e aborda várias áreas de otimização e gerenciamento de redes. Ele demonstra um ambiente simulado para testar diferentes técnicas de otimização e ajustes em uma rede Wi-Fi. Para uso em um cenário real, cada seção seria cuidadosamente adaptada e testada.

requirements
pip install numpy scikit-learn requests beautifulsoup4 dnspython
