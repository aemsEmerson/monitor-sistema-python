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

def mostrar_uso_memoria(memoria_total, memoria_usada, memoria_disponivel,porcentagem):
    print(50*"=")
    print("  Monitor do Sistema ")
    print(50*"=")
    print(f'Memória Total.....: {memoria_total:.2f} GB')              
    print(f'Memória Usada.....: {memoria_usada:.2f} GB')              
    print(f'Memória Livre.....: {memoria_disponivel:.2f} GB')              
    print(f'Uso da Memória....: {porcentagem:.2f}%')              
    
mostrar_uso_memoria(
    memoria_total,
    memoria_usada,
    memoria_disponivel,
    porcentagem
)
    


    
        
        
    
  

    
