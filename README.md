# 📸 Gerador de Dataset de Screenshots de Redes Sociais

Sistema automatizado para gerar screenshots autênticos e manipulados de redes sociais (Twitter/X, Instagram, WhatsApp) para treinamento de modelos de Machine Learning de detecção de adulterações.

## 🎯 Objetivo

Criar um dataset completo e realista para treinar modelos supervisionados (KNN, SVM, Árvores de Decisão) capazes de detectar screenshots manipulados de redes sociais.

## ✨ Características

- **Alta Fidelidade Visual**: Templates HTML/CSS 99% idênticos às interfaces reais
- **Totalmente Automatizado**: Um comando gera todo o dataset
- **Dados Fictícios**: Privacidade garantida - nenhum dado pessoal real
- **Manipulações Realistas**: Alterações sutis e moderadas que falsificadores reais fariam
- **Reprodutível**: Seed configurável para resultados consistentes

## 📊 Dataset Gerado

### Quantidade
- **60 screenshots autênticos** (20 de cada rede social)
- **180 screenshots manipulados** (3 variações de cada autêntico)
- **Total: 240 imagens**

### Redes Sociais
- Twitter/X
- Instagram
- WhatsApp

### Tipos de Manipulações

#### Twitter/X
- Alteração de métricas (curtidas, retweets, visualizações)
- Modificação do texto do tweet
- Adição/remoção de badge de verificado

#### Instagram
- Alteração de contagem de curtidas
- Modificação da caption
- Adição/remoção de badge de verificado

#### WhatsApp
- Alteração do conteúdo das mensagens
- Modificação do nome do contato
- Mudança de horários

### Arquivo labels.csv

Contém metadados completos de cada imagem:

| Coluna | Descrição |
|--------|-----------|
| `filename` | Nome do arquivo da imagem |
| `class` | `autentico` ou `manipulado` |
| `manipulation_type` | Tipo específico de manipulação aplicada |
| `original_filename` | Nome do screenshot autêntico relacionado |
| `social_network` | Rede social (twitter, instagram, whatsapp) |

## 🚀 Instalação

### Pré-requisitos
- Python 3.8+
- pip

### Passos

1. **Clone ou baixe este repositório**

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Instale o browser do Playwright:**
```bash
playwright install chromium
```

## 🎬 Uso

### Gerar o Dataset Completo

Execute o script principal:

```bash
python main.py
```

O processo levará aproximadamente **5-10 minutos** e você verá o progresso em tempo real:

```
🚀 Iniciando geração do dataset...
📊 Serão gerados: 60 autênticos + 180 manipulados
📁 Total: 240 imagens

📱 Gerando TWITTER...
  ✓ twitter_000.png
    ↳ twitter_000_manip_1.png (metrics_change)
    ↳ twitter_000_manip_2.png (text_change)
    ↳ twitter_000_manip_3.png (verification_change)
  ...

📱 Gerando INSTAGRAM...
  ...

📱 Gerando WHATSAPP...
  ...

✅ Dataset gerado com sucesso!
```

### Resultado

Após a execução, você terá:
- Pasta `dataset/autenticos/` com 60 screenshots originais
- Pasta `dataset/manipulados/` com 180 screenshots adulterados
- Arquivo `dataset/labels.csv` com todos os metadados

## 🔧 Configuração

Você pode ajustar parâmetros editando o arquivo `main.py`:

```python
# Seed para reprodutibilidade
SEED = 42

# Quantidade de posts por plataforma
POSTS_PER_PLATFORM = 20  # Altere para gerar mais ou menos

# Manipulações por post autêntico
MANIPULATIONS_PER_POST = 3
```

## 📁 Estrutura do Projeto

```
.
├── main.py                 # Script principal
├── requirements.txt        # Dependências Python
├── README.md              # Este arquivo
├── templates/             # Templates HTML das redes sociais
│   ├── twitter.html       # Template do Twitter/X
│   ├── instagram.html     # Template do Instagram
│   └── whatsapp.html      # Template do WhatsApp
└── dataset/               # Output (gerado automaticamente)
    ├── autenticos/
    ├── manipulados/
    └── labels.csv
```

## 🎨 Características Técnicas

### Geração de Dados Fictícios
- Biblioteca `Faker` para nomes, textos e dados realistas
- Avatares gerados como círculos coloridos com iniciais
- Métricas (curtidas, views, etc) com distribuições realistas
- Timestamps relativos (1h, 3d, etc)

### Templates HTML/CSS
- Réplicas de alta fidelidade (99% idênticas)
- Cores, fontes e espaçamentos autênticos
- Layouts responsivos mas com viewport fixo
- Ícones usando Unicode para simplicidade

### Screenshots
- Playwright para automação do browser
- Modo headless para performance
- Viewport configurado por rede social
- Formato PNG para preservar qualidade

### Manipulações
- Balanceadas (50% sutis, 50% moderadas)
- Alterações de métricas: ±20-50%
- Textos modificados usando Faker
- Badges de verificação adicionados/removidos
- Nomes e usernames alterados

## 🤖 Uso para Machine Learning

### Exemplos de Features para Extração

Este dataset foi projetado para permitir extração de features como:

- **LBP (Local Binary Patterns)**: Detectar inconsistências de textura
- **Análise RGB/HSV**: Identificar anomalias de cor
- **Haralick**: Analisar características de textura
- **Detecção de Bordas**: Encontrar artefatos de edição
- **Análise de Fontes**: Detectar inconsistências tipográficas
- **Metadados**: Padrões em números e timestamps

### Exemplo de Carregamento em Python

```python
import pandas as pd
from PIL import Image
import numpy as np

# Carregar labels
df = pd.read_csv('dataset/labels.csv')

# Filtrar apenas Twitter
twitter_df = df[df['social_network'] == 'twitter']

# Carregar uma imagem
img_path = f"dataset/{twitter_df.iloc[0]['class']}s/{twitter_df.iloc[0]['filename']}"
img = Image.open(img_path)
img_array = np.array(img)

# Extrair features...
```

## 🔬 Validação do Dataset

Recomendações para uso em pesquisa:

1. **Split Treino/Teste**: 80/20 ou 70/30
2. **Validação Cruzada**: K-fold para robustez
3. **Métricas**: Acurácia, Precisão, Recall, F1-Score
4. **Balanceamento**: Dataset já vem balanceado (1:3 ratio)

## ⚠️ Limitações

- Screenshots são simulações de alta fidelidade, não capturas reais
- Manipulações são programáticas, não editadas manualmente
- Não inclui manipulações de imagem avançadas (deepfakes, etc)
- Focado em alterações de texto e métricas
