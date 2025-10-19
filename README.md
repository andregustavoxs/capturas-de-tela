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
- **Alteração de métricas** (curtidas, retweets, visualizações): ±50% de variação
- **Modificação do texto**: Tweet alterado (garantidamente diferente do original)
- **Adição/remoção de badge de verificado**

#### Instagram
- **Alteração de curtidas**: ±50% de variação
- **Modificação da legenda (caption)**: Caption alterada (garantidamente diferente da original)
- **Adição/remoção de badge de verificado**

#### WhatsApp
- **Mudança de horários**: Todos os horários das mensagens são recriados aleatoriamente
- **Alteração do conteúdo das mensagens**: Conversa completa trocada (garantidamente diferente da original)
- **Modificação do nome do contato**: Nome alterado no cabeçalho

### Arquivo labels.csv

Contém metadados completos de cada imagem:

| Coluna | Descrição | Valores Possíveis |
|--------|-----------|-------------------|
| `filename` | Nome do arquivo da imagem | `twitter_000.png`, `instagram_005_manip_2.png`, etc |
| `class` | Se a imagem é autêntica ou manipulada | `autentico` ou `manipulado` |
| `manipulation_type` | Tipo específico de manipulação aplicada | `none`, `metrics_change`, `text_change`, `caption_change`, `message_change`, `time_change`, `verification_change`, `contact_change` |
| `original_filename` | Nome do screenshot autêntico relacionado | `twitter_005.png`, `instagram_010.png`, etc |
| `social_network` | Rede social da imagem | `twitter`, `instagram`, `whatsapp` |

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
>> Iniciando geracao do dataset...
>> Serao gerados: 60 autenticos + 180 manipulados
>> Total: 240 imagens

>> Gerando TWITTER...
  [OK] twitter_000.png
    -> twitter_000_manip_1.png (metrics_change)
    -> twitter_000_manip_2.png (text_change)
    -> twitter_000_manip_3.png (verification_change)
  ...

>> Gerando INSTAGRAM...
  [OK] instagram_000.png
    -> instagram_000_manip_1.png (metrics_change)
    -> instagram_000_manip_2.png (caption_change)
    -> instagram_000_manip_3.png (verification_change)
  ...

>> Gerando WHATSAPP...
  [OK] whatsapp_000.png
    -> whatsapp_000_manip_1.png (time_change)
    -> whatsapp_000_manip_2.png (message_change)
    -> whatsapp_000_manip_3.png (contact_change)
  ...

[SUCESSO] Dataset gerado com sucesso!
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
capturas-de-tela/
├── src/                          # 📦 Código-fonte modular
│   ├── __init__.py              # Exportações públicas do pacote
│   ├── config.py                # Configurações e constantes
│   ├── generators.py            # Funções de geração de dados fictícios
│   ├── screenshots.py           # Criação de screenshots autênticos
│   └── manipulations.py         # Aplicação de manipulações
│
├── templates/                    # 🎨 Templates HTML
│   ├── twitter.html             # Template do Twitter/X
│   ├── instagram.html           # Template do Instagram
│   └── whatsapp.html            # Template do WhatsApp
│
├── dataset/                      # 📊 Dataset gerado (criado automaticamente)
│   ├── autenticos/              # Screenshots originais
│   ├── manipulados/             # Screenshots adulterados
│   └── labels.csv               # Metadados e labels
│
├── main.py                       # 🚀 Script principal de execução
├── requirements.txt              # 📋 Dependências Python
└── README.md                     # 📖 Esta documentação
```

### Módulos do Pacote `src/`

#### `config.py`
Configurações centralizadas:
- Seed para reprodutibilidade (SEED = 42)
- Diretórios e caminhos
- Listas de conteúdo (tweets, captions, conversas em pt_BR)
- Cores de avatares
- Constantes de quantidade

#### `generators.py`
Funções de geração de dados:
- `generate_avatar_color()` - Cores aleatórias para avatares
- `get_initials(name)` - Extrai iniciais de nomes
- `generate_username(name)` - Cria usernames realistas
- `generate_tweet_text()` - Seleciona tweets realistas
- `generate_instagram_caption()` - Seleciona captions
- `generate_whatsapp_messages()` - Seleciona conversas
- `format_number(num)` - Formata métricas (1.5K, 2.3M)
- `generate_timestamp()` - Timestamps relativos (5h, 2d)
- `generate_time()` - Horários (HH:MM)

#### `screenshots.py`
Criação de screenshots:
- `create_twitter_screenshot(page, filename)` - Gera tweets
- `create_instagram_screenshot(page, filename)` - Gera posts
- `create_whatsapp_screenshot(page, filename)` - Gera conversas

Cada função retorna um dicionário com todos os dados gerados para permitir manipulações posteriores.

#### `manipulations.py`
Aplicação de alterações:
- `manipulate_twitter(page, data, tipo)` - Manipula tweets
- `manipulate_instagram(page, data, tipo)` - Manipula posts
- `manipulate_whatsapp(page, data, tipo)` - Manipula conversas

Suporta múltiplos tipos de manipulação por plataforma.

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
- **Alterações de métricas**: Quantidade de Curtidas
- **Textos modificados**: Usando Faker com **garantia de diferença** do original
  - Twitter: Tweets sempre diferentes
  - Instagram: Captions sempre diferentes
  - WhatsApp: Conversas sempre diferentes
- **Verificação de diferença**: Loop automático que regenera até obter texto diferente
- **Badges de verificação**: Adicionados/removidos aleatoriamente
- **Nomes e contatos**: Alterados usando Faker

---

**⚠️ Aviso Legal**: Este dataset é gerado sinteticamente e não contém dados reais de usuários. Todos os nomes, textos, números e informações são completamente fictícios, gerados pela biblioteca Faker. O projeto é destinado exclusivamente para fins educacionais e de pesquisa.
