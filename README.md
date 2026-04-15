# Replicador de Estrutura de Pastas (Python)

Este projeto replica **somente a organização das pastas** de uma origem para um destino, **sem copiar nenhum arquivo**.

## O que ele faz
- Lê toda a árvore de diretórios de uma pasta de origem
- Cria a mesma estrutura em uma nova pasta de saída
- **Ignora todos os arquivos**
- Salva por padrão a saída na pasta **Downloads** do usuário
- Gera um arquivo `relatorio_replicacao.txt` ao final

## Arquivos do projeto
- `replicador_estrutura.py` → script principal
- `executar_replicador.bat` → atalho para facilitar a execução no Windows
- `README.md` → este guia

## Como usar (modo interativo)
### Windows
1. Abra o **Prompt de Comando** dentro da pasta do projeto
2. Execute:

```bash
python replicador_estrutura.py
```

3. Informe:
   - caminho da pasta de origem
   - destino (ou pressione ENTER para usar Downloads)
   - nome da pasta de saída (ou ENTER para gerar automático)

### Exemplo
```bash
python replicador_estrutura.py
```

Depois, informe algo como:
```text
C:\Users\SeuUsuario\Documents\MinhaOrigem
```

Se pressionar ENTER no destino, a saída será criada em:
```text
C:\Users\SeuUsuario\Downloads
```

## Como usar por linha de comando (sem perguntas)
```bash
python replicador_estrutura.py "C:\\Origem\\MinhaPasta" --destino "C:\\Users\\SeuUsuario\\Downloads" --nome-saida "Estrutura_Replicada"
```

## Comportamento padrão
Se você não informar o destino, o script tenta usar automaticamente:
- `C:\Users\<usuario>\Downloads` no Windows
- `~/Downloads` em outros sistemas

## Saída gerada
O script cria uma pasta parecida com:
```text
Downloads\ESTRUTURA_VAZIA_MinhaPasta_20260415_140000
```

Dentro dela, ficará a estrutura vazia da pasta original e o relatório:
```text
relatorio_replicacao.txt
```

## Observação
Esse script **não move e não copia arquivos**. Ele apenas recria as pastas.
