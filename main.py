import time

def ler_memoria():
    with open("/proc/meminfo") as arquivo:
        
        linhas = arquivo.readlines()
        memoria = {}

        for linha in linhas:
        
            if linha.startswith('Mem'):
                nome, tamanho, unidade = linha.split()
                memoria[nome] = int(tamanho) / 1024**2
        return memoria
memoria = ler_memoria()


def calcular_memoria():
    memoria_total = float(memoria['MemTotal:'])
    memoria_disponivel = float(memoria['MemAvailable:'])
    memoria_usada = memoria_total - memoria_disponivel
    porcentagem = (memoria_usada / memoria_total) * 100
    return memoria_total, memoria_disponivel,memoria_usada, porcentagem
memoria_total, memoria_disponivel, memoria_usada, porcentagem = calcular_memoria()

def ler_cpu():
    with open("/proc/cpuinfo") as arquivo:

        linhas = arquivo.readlines()
        cpu = {}

        for linha in linhas:
            if linha.startswith(('model name', 'cpu cores','siblings')):

                name, value = linha.split(':')
                
                name = name.strip()
                value = value.strip()

                cpu[name] = value
        return cpu    
cpu = ler_cpu()

def ler_stat_cpu():

    with open ("/proc/stat") as arquivo:
        linhas = arquivo.readlines()
        stat_cpu = {}
        soma = 0

        for linha in linhas:
            
            if linha.startswith('cpu '):
                chave = ['title','user', 'nice', 'system','idle', 'iowait', 'irq', 'softirq', 'steal', 'guest', 'guest_nice']
                valor = linha.split()
                stat_cpu = dict(zip(chave,valor))
                stat_cpu.pop('title')

        for chave, valor in stat_cpu.items():
            stat_cpu[chave] = int(valor) 
            

        return stat_cpu
ler_stat_cpu()

def calculo_porcentagem_uso_cpu():
    primeira_leitura = ler_stat_cpu()
    time.sleep(1)
    segunda_leitura = ler_stat_cpu()

    total1 = sum(primeira_leitura.values())
    total2 = sum(segunda_leitura.values())
    delta_total = total2 - total1

    idle1 = primeira_leitura['idle']
    idle2 = segunda_leitura['idle']
    delta_idle = idle2 - idle1

    porcentagem_final = 100 * (1 - delta_idle / delta_total)
    return porcentagem_final
uso_cpu = calculo_porcentagem_uso_cpu()

def tratar_cpu():
    cpu['model name'] = cpu['model name'].replace("with", "GPU")
    cpu['siblings'] = int(cpu['siblings'])
    cpu['cpu cores'] = int(cpu['cpu cores'])
    return cpu

tratar_cpu()

def mostrar_uso_memoria(memoria_total, memoria_usada, memoria_disponivel,porcentagem):

    print(f'{15*'='} Monitor Sistema{15*"="}')
    print()
    print(f'MEMÓRIA')
    print(f'Memória Total.....: {memoria_total:.2f} GB')              
    print(f'Memória Usada.....: {memoria_usada:.2f} GB')              
    print(f'Memória Livre.....: {memoria_disponivel:.2f} GB')              
    print(f'Uso da Memória....: {porcentagem:.2f}%')     

def mostrar_cpu():
    print()
    print(f'CPU')
    print(f'{cpu['model name']}')
    print(f'Cores.....: {cpu['cpu cores']}')
    print(f'Threads.....: {cpu['siblings']}')
    print(f'Uso.....: {uso_cpu:.2f}%')



mostrar_uso_memoria(
    memoria_total,
    memoria_usada,
    memoria_disponivel,
    porcentagem
)

mostrar_cpu()


    
        
        
    
  

    
