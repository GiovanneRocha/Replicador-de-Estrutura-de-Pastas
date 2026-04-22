# Replicador de Estrutura de Pastas (Python)

Esta versão faz **varredura completa e profunda**, recriando **TODAS as pastas e subpastas**, inclusive **pastas dentro de pastas**, sem copiar arquivos.

## O que faz
- Lê toda a árvore da pasta de origem
- Varre todas as subpastas em profundidade completa
- Cria a mesma estrutura no destino
- Não copia arquivos
- Usa `Downloads` como destino padrão
- Gera `relatorio_replicacao.txt` com a lista completa das pastas criadas
- Exibe mensagem final de **PROCESSO COMPLETO**

## Arquivos
- `replicador_estrutura.py`
- `executar_replicador.bat`
- `README.md`

## Uso rápido (Windows)
1. Extraia o `.zip`
2. Abra a pasta extraída
3. Dê duplo clique em `executar_replicador.bat`
4. Informe:
   - pasta de origem
   - destino (ou pressione ENTER para usar Downloads)
   - nome da saída (ou ENTER para nome automático)

## Uso por comando
```bash
python replicador_estrutura.py "C:\Origem\MinhaPasta" --destino "C:\Users\SeuUsuario\Downloads" --nome-saida "Estrutura_Replicada"
```

## Saída esperada
O programa criará algo como:
```text
Downloads\ESTRUTURA_VAZIA_MinhaPasta_20260415_140000\MinhaPasta\...
```

E também:
```text
Downloads\ESTRUTURA_VAZIA_MinhaPasta_20260415_140000\relatorio_replicacao.txt
```

## Observação
Esta versão foi reforçada para garantir a recriação de **todas as camadas** da estrutura de diretórios.
