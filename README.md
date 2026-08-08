# Monitor de Sistemas em Python

Projeto desenvolvido durante meus estudos de Python com o objetivo de monitorar informações do sistema Linux.

## Sobre o projeto

Atualmente, o projeto realiza o monitoramento do uso de memória RAM, obtendo os dados diretamente do arquivo `/proc/meminfo`.


## Funcionalidades

- Ler informações de memória do sistema
- Cálculo da memória utilizada
- Cálculo da porcentagem de uso da memória
- Exibição das informações no terminal

## Tecnologias utilizadas

- Python3
- Linux
- `/proc/meminfo`

## Como executar

Clonar o repositório:

git clone git@github.com:aemsEmerson/monitor-sistema-python.git

Entre na pasta:

cd monitor-sistema-python

executar o programa:

python3 main.py

## Exemplo de saída

![Exemplo do Monitoramento](imagens/monitor-sistema.png)

## Evolução do projeto

- [x] Versão - 1.0 Monitoramento de memória RAM

## Próximas melhorias

- [ ] Monitoramento de CPU
- [ ] Monitoramento de armazenamento
- [ ] Monitoramento em tempo real

## Estrutura do Projeto

```text
monitor-sistema-python/
├── imagens/
│   └── sistema.png
├── main.py
├── README.md
└── .gitignore