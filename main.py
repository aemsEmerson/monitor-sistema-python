import time
import subprocess

def ler_memoria():
    with open("/proc/meminfo") as arquivo:
        
        linhas = arquivo.readlines()
        memoria = {}

        for linha in linhas:
            # Filtra somente as informações de memória que serão utilizadas no projeto
            if linha.startswith('Mem'):
                nome, tamanho, unidade = linha.split()
                # Os valores da memória de /proc/meminfo são fornecidos em KB e convertidos para GB
                memoria[nome] = int(tamanho) / 1024**2
        return memoria

def ler_cpu():
    # Abrindo o arquivo /proc/cpuinfo para buscar informações da CPU
    with open("/proc/cpuinfo") as arquivo:

        linhas = arquivo.readlines()
        cpu = {}

        for linha in linhas:
            # Filtra as informações relevantes para o projeto: modelo, núcleos e threads
            if linha.startswith(('model name', 'cpu cores','siblings')):

                name, value = linha.split(':')
                
                name = name.strip()
                value = value.strip()

                cpu[name] = value
        return cpu    

def ler_stat_cpu():
    # /proc/stat fornece informações sobre a CPU
    with open ("/proc/stat") as arquivo:
        linhas = arquivo.readlines()
        stat_cpu = {}

        for linha in linhas:
            # Seleciona a linha com os tempos gerais de uso da CPU para os cálculos posteriores
            if linha.startswith('cpu '):
                # Insere uma lista com as chaves do dicionário que iremos criar
                chave = ['title','user', 'nice', 'system','idle', 'iowait', 'irq', 'softirq', 'steal', 'guest', 'guest_nice']
                valor = linha.split()
                # Associa cada chave ao respectivo valor e cria o dicionário                
                stat_cpu = dict(zip(chave,valor))
                stat_cpu.pop('title')

        for chave, valor in stat_cpu.items():
            stat_cpu[chave] = int(valor) 
            
        return stat_cpu

def ler_disco():
    # O comando df fornece informações sobre o uso dos sistemas de arquivos
    resultado = subprocess.run(["df", "-h"], capture_output=True)
    resultado = resultado.stdout.decode()
    resultado = resultado.splitlines()
    disco = {}
    for linha in resultado:
        # Filtra a partição principal que será monitorada
        if linha.startswith('/dev/nvme0n1p2'):
            chave = ['dispositivo', 'tamanho', 'usado', 'disponivel', 'porcentagem', 'montado_em']
            dados_disco = linha.split()
            disco = dict(zip(chave, dados_disco))
            disco['porcentagem'] = int((disco['porcentagem']).replace('%', ''))       
    return disco

def calcular_memoria(memoria):
    # Memória total do dispositivo
    memoria_total = float(memoria['MemTotal:'])
    # Memória disponível no momento da leitura, utilizada nos cálculos    
    memoria_disponivel = float(memoria['MemAvailable:'])
    memoria_usada = memoria_total - memoria_disponivel
    porcentagem = (memoria_usada / memoria_total) * 100
    return memoria_total, memoria_disponivel,memoria_usada, porcentagem

def tratar_cpu(cpu):
    cpu['model name'] = cpu['model name'].replace("with", "GPU")
    cpu['siblings'] = int(cpu['siblings'])
    cpu['cpu cores'] = int(cpu['cpu cores'])
    
def calculo_porcentagem_uso_cpu():
    # Usa a função ler_stat_cpu para fazer uma primeira leitura dos valores da CPU
    primeira_leitura = ler_stat_cpu()
    # Espera 1 segundo
    time.sleep(1)
    # Realiza outra leitura para comparar com a primeira
    segunda_leitura = ler_stat_cpu()

    # Soma os valores de cada leitura
    total1 = sum(primeira_leitura.values())
    total2 = sum(segunda_leitura.values())
    # Calcula a diferença entre os totais
    delta_total = total2 - total1

    # Obtém o tempo ocioso da CPU em cada leitura
    idle1 = primeira_leitura['idle']
    idle2 = segunda_leitura['idle']
    # Calcula a diferença entre os tempos ociosos
    delta_idle = idle2 - idle1

    # Fórmula para cálculo da porcentagem de CPU usada
    # Usa os parâmetros calculados acima e aplica-os à fórmula
    porcentagem_final = 100 * (1 - delta_idle / delta_total)
    return porcentagem_final

def mostrar_uso_memoria(memoria_total, memoria_usada, memoria_disponivel,porcentagem):
    print(f'MEMÓRIA')
    print(f'Memória Total.....: {memoria_total:.2f} GB')              
    print(f'Memória Usada.....: {memoria_usada:.2f} GB')              
    print(f'Memória Livre.....: {memoria_disponivel:.2f} GB')              
    print(f'Uso da Memória....: {porcentagem:.2f}%')  
    print()   

def mostrar_cpu(cpu, uso_cpu):
    print(f'CPU')
    print(f'{cpu['model name']}')
    print(f'Cores....: {cpu['cpu cores']}')
    print(f'Threads..: {cpu['siblings']}')
    print(f'Uso......: {uso_cpu:.2f}%')
    print()

def mostrar_disco(disco):
    print('DISCO')
    print(f'Tamanho...........: {disco['tamanho']}')
    print(f'Usado.............: {disco['usado']}')
    print(f'Disponivel........: {disco['disponivel']}')
    print(f'% de uso do disco.: {disco['porcentagem']}%')

memoria = ler_memoria()
cpu = ler_cpu()
info_disco = ler_disco()

memoria_total, memoria_disponivel, memoria_usada, porcentagem = calcular_memoria(memoria)
tratar_cpu(cpu)
uso_cpu = calculo_porcentagem_uso_cpu()

print(f'{15*'='} Monitor Sistema{15*"="}')
print()
mostrar_uso_memoria(
    memoria_total,
    memoria_usada,
    memoria_disponivel,
    porcentagem
)
mostrar_cpu(cpu, uso_cpu)

mostrar_disco(info_disco)


    
        
        
    
  

    
