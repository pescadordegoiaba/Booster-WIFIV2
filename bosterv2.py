#!/usr/bin/env python3
import subprocess
import time
import numpy as np
from sklearn.linear_model import LinearRegression
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
import dns.resolver
import random

def measure_latency(destination, packets):
    try:
        result = subprocess.run(['ping', '-c', str(packets), destination], stdout=subprocess.PIPE, text=True)
        latencies = []
        for line in result.stdout.splitlines():
            if "time=" in line:
                latency = float(line.split("time=")[-1].split()[0])
                latencies.append(latency)
        return latencies
    except Exception as e:
        print(f"Erro ao medir latência: {e}")
        return []

class CongestionModel:
    def __init__(self):
        self.model = None

    def train_model(self, latencies):
        if len(latencies) < 2:
            print("Não há dados suficientes para ajustar o modelo.")
            return

        X = np.arange(len(latencies)).reshape(-1, 1)
        y = latencies

        self.model = LinearRegression()
        self.model.fit(X, y)
        print("Modelo de congestão treinado com sucesso.")

    def predict_congestion_score(self, num_data_points):
        if not self.model:
            print("O modelo não foi treinado ainda.")
            return None

        congestion_score = self.model.predict(np.array([[num_data_points]]))
        return congestion_score

def adjust_congestion_control(latencies):
    model = CongestionModel()
    model.train_model(latencies)

    return model

# Exemplo de uso
latency_data = [45, 40, 50, 55, 60]  # Latências observadas

congestion_model = adjust_congestion_control(latency_data)
congestion_score = congestion_model.predict_congestion_score(len(latency_data))

if congestion_score is not None:
    print(f"Score de Congestionamento: {congestion_score}")


def set_tcp_window_scaling(value):
    subprocess.run(['sysctl', '-w', f"net.ipv4.tcp_window_scaling={value}"])

def adjust_congestion_window(latency_data, current_window_size):
    avg_latency = sum(latency_data) / len(latency_data)
    weighted_avg_latency = sum((i + 1) * latency for i, latency in enumerate(latency_data)) / sum(range(1, len(latency_data) + 1))

    target_latency = 30  # Alvo desejado para a latência média (ajuste conforme necessário)
    max_window_size = 200  # Tamanho máximo da janela de congestionamento
    min_window_size = 50   # Tamanho mínimo da janela de congestionamento

    if avg_latency > target_latency:
        # Diminui a janela de congestionamento de forma gradual e proporcional à diferença de latência
        decrease_factor = 0.9 - (avg_latency - target_latency) * 0.02
        new_window_size = int(current_window_size * decrease_factor)
    else:
        # Aumenta a janela de congestionamento de forma proporcional à melhora na latência
        increase_factor = 1.0 + (target_latency - avg_latency) * 0.01
        new_window_size = int(current_window_size * increase_factor)

    # Limita a janela dentro dos intervalos aceitáveis
    new_window_size = max(min_window_size, min(new_window_size, max_window_size))

    print(f"Ajustando a janela de congestionamento para {new_window_size}")
    set_tcp_window_scaling(new_window_size)
    print("Janela de congestionamento ajustada.")

# Exemplo de uso
current_window_size = 80  # Valor inicial da janela de congestionamento
latency_data = [45, 40, 50]  # Latências observadas

adjust_congestion_window(latency_data, current_window_size)


def set_dns_servers(dns_servers):
    with open('/etc/resolv.conf', 'w') as resolv_conf:
        for server in dns_servers:
            resolv_conf.write(f'nameserver {server}\n')

def optimize_dns():
    try:
        print("Otimizando configurações de DNS...")
        
        custom_dns_servers = ["8.8.8.8", "8.8.4.4"]  # Substitua pelos seus servidores DNS preferidos
        
        # Consulta os servidores DNS para verificar a disponibilidade
        resolver = dns.resolver.Resolver()
        resolver.timeout = 1
        resolver.lifetime = 1
        
        available_servers = []
        for server in custom_dns_servers:
            try:
                resolver.nameservers = [server]
                answer = resolver.resolve("google.com")
                print(f"Servidor DNS {server} disponível.")
                available_servers.append(server)
            except dns.exception.Timeout:
                print(f"Timeout ao consultar o servidor DNS {server}.")
            except dns.resolver.NoNameservers:
                print(f"Não há servidores DNS para o domínio {server}.")
        
        if available_servers:
            set_dns_servers(available_servers)
            print("Configurações de DNS otimizadas.")
        else:
            print("Nenhum servidor DNS disponível para otimização.")
    except Exception as e:
        print(f"Erro ao otimizar configurações de DNS: {e}")

def get_all_resources():
    url = "https://data.jsdelivr.com/v1/stats/packages"
    response = requests.get(url)
    data = response.json()
    resources = []

    for package in data:
        if 'assets' in package:
            resources.extend(package['assets'])

    return resources

def accelerate_content_with_cdn():
    cdn_url = "https://cdn.jsdelivr.net"
    
    resources = get_all_resources()
    
    print("Acelerando conteúdo com CDN...")
    
    try:
        for resource in resources:
            url = cdn_url + resource
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Recurso {resource} acelerado com CDN.")
            else:
                print(f"Não foi possível acelerar o recurso {resource}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Erro ao acelerar conteúdo com CDN: {e}")

def set_tcp_parameter(parameter, value):
    subprocess.run(['sysctl', '-w', f'{parameter}={value}'])

def optimize_tcp_parameters():
    parameters = [
        {'parameter': 'net.ipv4.tcp_window_scaling', 'value': 0},
        {'parameter': 'net.core.rmem_max', 'value': 16777216},  # Exemplo: 16 MB
        {'parameter': 'net.core.wmem_max', 'value': 16777216},  # Exemplo: 16 MB
        # Adicione mais parâmetros conforme necessário
    ]
    
    # Adicionando parâmetros de tamanho de buffer crescente
    buffer_sizes_kb = [200, 300, 500, 600, 700, 1000, 2000, 3000, 4000, 5000, 10000, 20000]
    for size_kb in buffer_sizes_kb:
        parameters.append({'parameter': 'net.ipv4.tcp_rmem', 'value': f'4096 87380 {size_kb * 1024}'})
        parameters.append({'parameter': 'net.ipv4.tcp_wmem', 'value': f'4096 65536 {size_kb * 1024}'})
    
    # Aplicando as configurações
    for param in parameters:
        set_tcp_parameter(param['parameter'], param['value'])

# Chame a função para otimizar os parâmetros
optimize_tcp_parameters()

def continuous_monitoring():
    # Implemente a lógica para monitoramento contínuo
    pass


configurations_applied = False  # Variável para controlar se as configurações já foram aplicadas

def measure_max_tx_power(interface):
    try:
        result = subprocess.run(['sudo', 'iw', interface, 'info'], stdout=subprocess.PIPE, text=True)
        lines = result.stdout.splitlines()
        for line in lines:
            if "max tx power" in line:
                return int(line.split(":")[-1])
        return None
    except Exception as e:
        print(f"Erro ao medir a potência de transmissão máxima: {e}")
        return None

def set_wifi_power_management(interface, state):
    try:
        subprocess.run(['sudo', 'iwconfig', interface, 'power', state], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Gerenciamento de energia configurado para {state}.")
    except Exception as e:
        print(f"Erro ao configurar o gerenciamento de energia: {e}")

def set_wifi_tx_power(interface, power_level):
    try:
        subprocess.run(['sudo', 'iw', interface, 'set', 'txpower', 'fixed', str(power_level)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Potência de transmissão configurada para {power_level} dBm.")
    except Exception as e:
        print(f"Erro ao configurar a potência de transmissão: {e}")

def set_wifi_antenna_mode(interface, mode):
    try:
        subprocess.run(['sudo', 'iw', interface, 'set', 'antenna', mode], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Modo de antena configurado para {mode}.")
    except Exception as e:
        print(f"Erro ao configurar o modo de antena: {e}")

def set_wifi_rate(interface, rate):
    try:
        subprocess.run(['sudo', 'iw', interface, 'set', 'bitrates', rate], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Taxa de bits configurada para {rate}.")
    except Exception as e:
        print(f"Erro ao configurar a taxa de bits: {e}")




class WiFiAP:
    def __init__(self, name, signal_strength):
        self.name = name
        self.signal_strength = signal_strength

class RoamingOptimizer:
    def __init__(self, ap_list):
        self.ap_list = ap_list
        self.current_ap = random.choice(ap_list)
    
    def detect_weak_ap(self):
        weak_aps = [ap for ap in self.ap_list if ap.signal_strength < self.current_ap.signal_strength]
        return weak_aps
    
    def check_latency(self, ap):
        # Simulando a verificação de latência
        return random.uniform(10, 100)
    
    def initiate_roaming(self):
        weak_aps = self.detect_weak_ap()
        
        if weak_aps:
            print("Detectou pontos de acesso fracos:", [ap.name for ap in weak_aps])
            for ap in weak_aps:
                latency = self.check_latency(ap)
                print(f"Latência para {ap.name}: {latency} ms")
            
            best_ap = min(weak_aps, key=lambda ap: self.check_latency(ap))
            print(f"Roaming para {best_ap.name}")
            self.current_ap = best_ap
        else:
            print("Não foram encontrados pontos de acesso fracos.")

# Exemplo de uso
ap1 = WiFiAP("AP1", 80)  # Nome e intensidade do sinal
ap2 = WiFiAP("AP2", 60)
ap3 = WiFiAP("AP3", 70)
ap_list = [ap1, ap2, ap3]

roaming_optimizer = RoamingOptimizer(ap_list)


class WiFiChannel:
    def __init__(self, channel_number, interference_level):
        self.channel_number = channel_number
        self.interference_level = interference_level

class ChannelOptimizer:
    def __init__(self, channel_list):
        self.channel_list = channel_list
        self.current_channel = random.choice(channel_list)
    
    def analyze_channels(self):
        print("Analisando canais disponíveis:")
        for channel in self.channel_list:
            print(f"Canal {channel.channel_number}: Interferência {channel.interference_level}")
    
    def choose_optimal_channel(self):
        optimal_channel = min(self.channel_list, key=lambda channel: channel.interference_level)
        return optimal_channel
    
    def optimize_channel(self):
        self.analyze_channels()
        optimal_channel = self.choose_optimal_channel()
        
        if optimal_channel != self.current_channel:
            print(f"Mudando para o Canal {optimal_channel.channel_number}")
            self.current_channel = optimal_channel
        else:
            print(f"Continuando no Canal {self.current_channel.channel_number}")

# Exemplo de uso
channel1 = WiFiChannel(1, 3)  # Número do canal e nível de interferência
channel2 = WiFiChannel(6, 2)
channel3 = WiFiChannel(11, 1)
channel_list = [channel1, channel2, channel3]

channel_optimizer = ChannelOptimizer(channel_list)



class AP:
    def __init__(self, name, initial_power):
        self.name = name
        self.power = initial_power

class PowerManager:
    def __init__(self, ap_list):
        self.ap_list = ap_list
    
    def monitor_network_load(self):
        # Simulando a carga da rede e a demanda de tráfego
        return random.uniform(0, 1)
    
    def adjust_power(self, ap):
        load = self.monitor_network_load()
        
        if load > 0.7:  # Alta carga
            ap.power = max(30, ap.power - 10)
            print(f"Reduzindo potência de transmissão de {ap.name} para {ap.power}")
        else:  # Baixa carga
            ap.power = min(100, ap.power + 10)
            print(f"Aumentando potência de transmissão de {ap.name} para {ap.power}")

# Exemplo de uso
ap1 = AP("AP1", 70)  # Nome do AP e potência inicial
ap2 = AP("AP2", 80)
ap_list = [ap1, ap2]

power_manager = PowerManager(ap_list)



class QW:
    def __init__(self, name, initial_bitrate):
        self.name = name
        self.bitrate = initial_bitrate

class BitrateManager:
    def __init__(self, qw_list):
        self.qw_list = qw_list
    
    def monitor_signal_quality(self, qw):
        # Simulando a qualidade do sinal e a taxa de perda de pacotes
        signal_quality = random.uniform(0, 1)  # Quanto maior, melhor
        packet_loss_rate = random.uniform(0, 0.2)  # Taxa de perda de pacotes
        
        return signal_quality, packet_loss_rate
    
    def adjust_bitrate(self, qw):
        signal_quality, packet_loss_rate = self.monitor_signal_quality(qw)
        
        if signal_quality < 0.4 or packet_loss_rate > 0.1:  # Qualidade ruim ou muita perda de pacotes
            qw.bitrate = max(1, qw.bitrate // 2)
            print(f"Reduzindo taxa de bits de {qw.name} para {qw.bitrate}")
        else:  # Boa qualidade e pouca perda de pacotes
            qw.bitrate = min(100, qw.bitrate * 2)
            print(f"Aumentando taxa de bits de {qw.name} para {qw.bitrate}")

# Exemplo de uso
qw1 = QW("AP1", 50)  # Nome do AP e taxa de bits inicial
qw2 = QW("AP2", 70)
qw_list = [qw1, qw2]

bitrate_manager = BitrateManager(qw_list)


class Fuel:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

class PacketQueue:
    def __init__(self):
        self.queue = []
    
    def enqueue(self, fuel):
        self.queue.append(fuel)
    
    def dequeue(self):
        if self.queue:
            return self.queue.pop(0)
        return None
    
    def prioritize_queue(self):
        self.queue.sort(key=lambda fuel: fuel.priority, reverse=True)

class TrafficController:
    def __init__(self, packet_queue):
        self.packet_queue = packet_queue
    
    def add_packets(self):
        # Simulando a chegada de pacotes com diferentes prioridades
        priorities = [1, 2, 3]
        for i in range(10):
            fuel = Fuel(f"Packet{i}", random.choice(priorities))
            self.packet_queue.enqueue(fuel)
            print(f"Pacote {fuel.name} adicionado à fila com prioridade {fuel.priority}")
    
    def process_packets(self):
        while self.packet_queue.queue:
            packet = self.packet_queue.dequeue()
            print(f"Processando pacote {packet.name} com prioridade {packet.priority}")
            time.sleep(1)  # Simula o tempo de processamento

# Exemplo de uso
packet_queue = PacketQueue()
traffic_controller = TrafficController(packet_queue)







if __name__ == "__main__":
    destination_address = "google.com"  # Altere para o destino desejado
    num_packets = 13  # Número de pacotes para enviar
    wifi_interface = "wlan0"  # Interface Wi-Fi, substitua pela sua

    if not configurations_applied:
        # Medir a potência de transmissão máxima
        max_tx_power = measure_max_tx_power(wifi_interface)
        if max_tx_power is not None:
            print(f"Potência de transmissão máxima suportada: {max_tx_power} dBm")

        # Configurações para maximizar o desempenho
        set_wifi_power_management(wifi_interface, "off")  # Desativar gerenciamento de energia
        set_wifi_tx_power(wifi_interface, 30)  # Ajustar potência de transmissão (valor em dBm)
        set_wifi_antenna_mode(wifi_interface, "auto")  # Modo de antena (auto ou 2.4GHz / 5GHz)
        set_wifi_rate(wifi_interface, "MCS 7")  # Configurar a taxa de bits (exemplo: MCS 7)
        configurations_applied = True

        print("Desempenho da placa Wi-Fi maximizado.")
    else:
        print("Não foi possível medir a potência de transmissão máxima.")

    while True:
        latency_data = measure_latency(destination_address, num_packets)
        congestion_model = adjust_congestion_control(latency_data)
        congestion_score = congestion_model.predict_congestion_score(len(latency_data))

        #FUEL
        traffic_controller.add_packets()
        packet_queue.prioritize_queue()
        traffic_controller.process_packets()
        

        #AI BITS
        for qw in bitrate_manager.qw_list:
         bitrate_manager.adjust_bitrate(qw)

        #AI Wifi
        for ap in power_manager.ap_list:
         power_manager.adjust_power(ap)

        print(f"Medições de latência: {latency_data}")
        print(f"Score de Congestionamento: {congestion_score}")
        print(f"Conectado a {roaming_optimizer.current_ap.name}")

        # Lógica para ajustar parâmetros de acordo com o congestionamento
        adjust_congestion_window(latency_data, current_window_size)

        # Otimização de DNS
        optimize_dns()

        # Aceleração de Conteúdo com CDN
        accelerate_content_with_cdn()

        # Otimização de TCP/IP
        # optimize_tcp_parameters()
        optimize_tcp_parameters()

        #roaming
        roaming_optimizer.initiate_roaming()

        #channel optimizer
        channel_optimizer.optimize_channel()

        time.sleep(3)  # Espera 5 segundos antes de medir novamente