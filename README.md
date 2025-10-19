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

## ✅ Garantias de Qualidade

### Textos Sempre Diferentes

O sistema implementa verificação automática para garantir que **100% das manipulações de texto sejam realmente diferentes dos originais**:

```python
# Exemplo de verificação implementada
new_text = generate_text()
while new_text == original_text:
    new_text = generate_text()
# Garante que new_text != original_text
```

**Benefícios:**
- Elimina a probabilidade de 5% (1/20) de colisão aleatória
- Evita falsos positivos no treinamento
- Garante qualidade consistente do dataset

### Tipos de Manipulação por Plataforma

| Plataforma | Tipo 1 (manip_1) | Tipo 2 (manip_2) | Tipo 3 (manip_3) |
|------------|------------------|------------------|------------------|
| **Twitter** | `metrics_change` | `text_change` | `verification_change` |
| **Instagram** | `metrics_change` | `caption_change` | `verification_change` |
| **WhatsApp** | `time_change` | `message_change` | `contact_change` |

**Observação:** WhatsApp usa `time_change` pois não possui métricas públicas como as outras plataformas.

## 💻 Exemplos de Uso do Dataset

### Carregar e Explorar os Dados

```python
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

# Carregar metadados
df = pd.read_csv('dataset/labels.csv')

# Estatísticas gerais
print("=== ESTATÍSTICAS DO DATASET ===")
print(f"Total de imagens: {len(df)}")
print(f"\nPor classe:")
print(df['class'].value_counts())
print(f"\nPor rede social:")
print(df['social_network'].value_counts())
print(f"\nPor tipo de manipulação:")
print(df['manipulation_type'].value_counts())

# Visualizar uma imagem
img_path = 'dataset/autenticos/twitter_000.png'
img = Image.open(img_path)
plt.imshow(img)
plt.axis('off')
plt.title('Exemplo de Screenshot Autêntico')
plt.show()
```

### Preparar Dataset para ML com PyTorch

```python
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import pandas as pd

class ScreenshotDataset(Dataset):
    """Dataset de screenshots de redes sociais"""

    def __init__(self, csv_file, root_dir, transform=None):
        """
        Args:
            csv_file (str): Caminho para labels.csv
            root_dir (str): Diretório raiz do dataset
            transform (callable, optional): Transformações da imagem
        """
        self.labels = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        # Obter informações
        row = self.labels.iloc[idx]
        img_name = row['filename']
        img_class = row['class']

        # Determinar subdiretório
        subdir = 'autenticos' if img_class == 'autentico' else 'manipulados'
        img_path = f"{self.root_dir}/{subdir}/{img_name}"

        # Carregar imagem
        image = Image.open(img_path).convert('RGB')

        # Label: 0 = autêntico, 1 = manipulado
        label = 0 if img_class == 'autentico' else 1

        # Aplicar transformações
        if self.transform:
            image = self.transform(image)

        return image, label, row['social_network']

# Transformações
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                       std=[0.229, 0.224, 0.225])
])

# Criar dataset
dataset = ScreenshotDataset(
    csv_file='dataset/labels.csv',
    root_dir='dataset',
    transform=transform
)

# Criar DataLoader
dataloader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True,
    num_workers=4
)

# Usar no treinamento
for images, labels, networks in dataloader:
    # Treinar modelo
    outputs = model(images)
    loss = criterion(outputs, labels)
    # ...
```

### Treinar Classificador Simples com Scikit-learn

```python
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import numpy as np
from PIL import Image

def extract_features(img_path):
    """Extrai features simples da imagem"""
    img = Image.open(img_path).convert('L')  # Grayscale
    img_array = np.array(img)

    # Features básicas
    features = {
        'mean': img_array.mean(),
        'std': img_array.std(),
        'min': img_array.min(),
        'max': img_array.max()
    }
    return list(features.values())

# Carregar dados
df = pd.read_csv('dataset/labels.csv')

# Extrair features
X = []
y = []

for _, row in df.iterrows():
    subdir = 'autenticos' if row['class'] == 'autentico' else 'manipulados'
    img_path = f"dataset/{subdir}/{row['filename']}"

    features = extract_features(img_path)
    X.append(features)
    y.append(0 if row['class'] == 'autentico' else 1)

X = np.array(X)
y = np.array(y)

# Split treino/teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Treinar modelo
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

# Avaliar
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred,
                          target_names=['Autêntico', 'Manipulado']))
print("\nMatriz de Confusão:")
print(confusion_matrix(y_test, y_pred))
```

### Filtrar por Tipo de Manipulação

```python
import pandas as pd

df = pd.read_csv('dataset/labels.csv')

# Apenas manipulações de texto do Twitter
twitter_text = df[
    (df['social_network'] == 'twitter') &
    (df['manipulation_type'] == 'text_change')
]

print(f"Total de tweets com texto manipulado: {len(twitter_text)}")

# Apenas alterações de verificação
verification_changes = df[
    df['manipulation_type'] == 'verification_change'
]

print(f"Total de mudanças de verificação: {len(verification_changes)}")

# Todas as manipulações de métricas
metrics_changes = df[
    df['manipulation_type'] == 'metrics_change'
]

print(f"Total de alterações de métricas: {len(metrics_changes)}")
```

## 🛠️ Desenvolvimento e Personalização

### Adicionar Novos Conteúdos

Para adicionar novos textos realistas, edite `src/config.py`:

```python
# Adicione novos tweets
REAL_TWEETS = [
    "Seu novo tweet aqui...",
    "Outro tweet realista...",
    # ... seus tweets
]

# Adicione novas captions
REAL_CAPTIONS = [
    "Nova caption inspiradora 💫",
    "Outro momento especial ✨",
    # ... suas captions
]

# Adicione novas conversas
REAL_CONVERSATIONS = [
    [
        ("Sua mensagem", "received"),
        ("Sua resposta", "sent"),
    ],
    # ... suas conversas
]
```

### Modificar Quantidade de Dados

No arquivo `src/config.py`:

```python
# Alterar quantidade de posts por rede social
POSTS_PER_PLATFORM = 50  # Padrão: 20

# Alterar quantidade de manipulações por post
MANIPULATIONS_PER_POST = 5  # Padrão: 3

# Com essas configurações:
# Total autênticos: 50 * 3 = 150
# Total manipulados: 150 * 5 = 750
# Total geral: 900 imagens
```

### Personalizar Templates HTML

Os templates estão em `templates/`. Para modificar:

1. Abra o arquivo HTML (twitter.html, instagram.html ou whatsapp.html)
2. Edite CSS para mudar cores, fontes, espaçamentos
3. Modifique estrutura HTML (mas mantenha os IDs dos elementos)
4. Teste executando o gerador

**Importante**: Não remova os `id` dos elementos pois o código JavaScript depende deles.

### Adicionar Nova Plataforma

Para adicionar uma nova rede social:

1. **Crie o template HTML** em `templates/nova_rede.html`
2. **Adicione função de criação** em `src/screenshots.py`:
   ```python
   async def create_nova_rede_screenshot(page, filename):
       # Implementar lógica
       pass
   ```
3. **Adicione função de manipulação** em `src/manipulations.py`:
   ```python
   async def manipulate_nova_rede(page, data, tipo):
       # Implementar lógica
       pass
   ```
4. **Registre no main.py**:
   ```python
   platforms = [
       ('twitter', create_twitter_screenshot, manipulate_twitter),
       ('instagram', create_instagram_screenshot, manipulate_instagram),
       ('whatsapp', create_whatsapp_screenshot, manipulate_whatsapp),
       ('nova_rede', create_nova_rede_screenshot, manipulate_nova_rede),
   ]
   ```

## 🧪 Testes e Verificação

### Testar Importações

```bash
python3 -c "from src import config, generators, screenshots, manipulations; print('✓ Todos os módulos OK')"
```

### Verificar Dataset Gerado

```python
import pandas as pd
from pathlib import Path

# Verificar estrutura
df = pd.read_csv('dataset/labels.csv')

# Checks básicos
assert len(df) == 240, "Deveria ter 240 imagens"
assert df['class'].value_counts()['autentico'] == 60
assert df['class'].value_counts()['manipulado'] == 180

# Verificar arquivos existem
for _, row in df.iterrows():
    subdir = 'autenticos' if row['class'] == 'autentico' else 'manipulados'
    filepath = Path(f"dataset/{subdir}/{row['filename']}")
    assert filepath.exists(), f"Arquivo não encontrado: {filepath}"

print("✓ Dataset verificado com sucesso!")
```

## 📚 Referências e Recursos

### Bibliotecas Utilizadas

- **[Playwright](https://playwright.dev/)** - Automação de navegadores
- **[Faker](https://faker.readthedocs.io/)** - Geração de dados fictícios
- **[Pandas](https://pandas.pydata.org/)** - Manipulação de dados tabulares
- **[Pillow](https://pillow.readthedocs.io/)** - Processamento de imagens

### Artigos Relacionados

- Detecção de Deepfakes e Imagens Manipuladas
- Computer Vision para Análise de Screenshots
- Datasets Sintéticos em Machine Learning

## ⚠️ Limitações e Considerações

### Limitações Conhecidas

1. **Variação Visual Limitada**: Mesmo usando seed aleatória, os templates HTML são fixos
2. **Sem Imagens Reais**: Posts não contêm fotos, apenas elementos de interface
3. **Idioma**: Conteúdo apenas em português brasileiro
4. **Plataformas**: Apenas 3 redes sociais (Twitter, Instagram, WhatsApp)

### Sugestões para Melhorias

- Adicionar variações de tema (claro/escuro)
- Incluir imagens aleatórias nos posts
- Suportar mais idiomas
- Adicionar TikTok, Facebook, LinkedIn
- Manipulações mais sofisticadas (fontes, espaçamento)

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. **Fork** o projeto
2. Crie uma **branch** para sua feature (`git checkout -b feature/MinhaFeature`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. **Push** para a branch (`git push origin feature/MinhaFeature`)
5. Abra um **Pull Request**

### Diretrizes de Código

- Siga PEP 8 para estilo Python
- Adicione docstrings em todas as funções
- Mantenha a estrutura modular
- Teste suas alterações antes de submeter

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos (PBL-3).

## 👥 Autores

**PBL-3 Team** - Universidade Estadual de Feira de Santana

## 📞 Suporte

Para dúvidas, problemas ou sugestões:
- Abra uma [issue](https://github.com/seu-repo/issues)
- Entre em contato com a equipe

---

**⚠️ Aviso Legal**: Este dataset é gerado sinteticamente e não contém dados reais de usuários. Todos os nomes, textos, números e informações são completamente fictícios, gerados pela biblioteca Faker. O projeto é destinado exclusivamente para fins educacionais e de pesquisa.