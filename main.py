"""
Gerador de Dataset de Screenshots de Redes Sociais
Cria screenshots autênticos e manipulados para treinamento de modelos ML
"""

import os
import random
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple

from faker import Faker
from playwright.async_api import async_playwright, Page
from PIL import Image, ImageDraw, ImageFont
import pandas as pd

# Configurações
SEED = 42
random.seed(SEED)
Faker.seed(SEED)

fake = Faker('pt_BR')

# Diretórios
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
DATASET_DIR = BASE_DIR / "dataset"
AUTHENTIC_DIR = DATASET_DIR / "autenticos"
MANIPULATED_DIR = DATASET_DIR / "manipulados"

# Criar diretórios se não existirem
AUTHENTIC_DIR.mkdir(parents=True, exist_ok=True)
MANIPULATED_DIR.mkdir(parents=True, exist_ok=True)

# Quantidades
POSTS_PER_PLATFORM = 20
MANIPULATIONS_PER_POST = 3

# Lista para armazenar metadados
dataset_metadata = []


# ============================================================================
# FUNÇÕES AUXILIARES - GERAÇÃO DE DADOS
# ============================================================================

# Textos realistas para tweets
REAL_TWEETS = [
    "Acabei de assistir esse filme e não consigo parar de pensar nele. Simplesmente incrível!",
    "Alguém mais acha que segunda-feira deveria ser cancelada? Quem concorda?",
    "Café da manhã perfeito: pão na chapa, café passado e um bom livro. Vida simples é vida feliz.",
    "O trânsito hoje está impossível. 2 horas pra chegar no trabalho, isso não é vida.",
    "Esse governo precisa entender que educação é prioridade. Investir em escola é investir no futuro.",
    "Recém voltei da praia e já estou com saudade. Final de semana passou voando!",
    "Tecnologia avançando e a gente aqui ainda com internet lenta. Brasil precisa melhorar muito.",
    "Parabéns pra todos os professores que fazem a diferença! Vocês são essenciais.",
    "Nada como um bom churrasco no domingo com a família. Tradição que nunca morre!",
    "Importante: vacinem suas crianças. Ciência salva vidas, fake news mata.",
    "Clima tá maluco. Calor de 40 graus num dia e chuva torrencial no outro.",
    "Se você ainda não assistiu aquela série nova, tá perdendo tempo. Melhor coisa do ano.",
    "Mercado tá caro demais. Comprei 3 coisas e gastei uma fortuna.",
    "Música boa é aquela que te faz parar tudo e só sentir. Hoje foi assim.",
    "Acabei de terminar um projeto que levou meses. Sensação de dever cumprido!",
    "Saúde mental importa. Cuidem de vocês, busquem ajuda quando necessário.",
    "Time jogou muito mal hoje. Não dá pra perder um jogo desses em casa.",
    "Alguém tem dica de livro bom? Terminei o último e tô perdido sem saber o que ler.",
    "Respeitem os entregadores. Eles trabalham muito e merecem reconhecimento.",
    "Dia de sol, praia lotada e água de coco gelada. É disso que eu gosto!",
]

# Captions realistas para Instagram
REAL_CAPTIONS = [
    "Dias simples são os melhores ☀️",
    "Aquele momento que a gente não esquece ✨",
    "Felicidade é estar com quem importa 💙",
    "Novas memórias sendo criadas 📸",
    "Vivendo um dia de cada vez",
    "Gratidão por mais um dia incrível 🙏",
    "A vida é feita de pequenos momentos",
    "Energia boa, pessoas melhores ✨",
    "Sorria, a vida é curta demais",
    "Momentos que viram saudade 💛",
    "Paz interior é tudo que precisamos",
    "Fim de semana do jeito que a gente ama",
    "Natureza curando a alma 🌿",
    "Café e boas conversas ☕",
    "Pôr do sol que aquece o coração",
    "Família é onde a vida começa ❤️",
    "Ser feliz é uma escolha diária",
    "Aventuras que ficam pra sempre",
    "Momentos perfeitos existem sim",
    "Aproveitar o agora é essencial",
]

# Conversas realistas para WhatsApp
REAL_CONVERSATIONS = [
    [
        ("E aí, conseguiu resolver aquele problema?", "received"),
        ("Consegui sim! Deu tudo certo no final", "sent"),
        ("Que bom! Fiquei preocupado", "received"),
        ("Obrigado por perguntar!", "sent"),
    ],
    [
        ("Vamos marcar aquele almoço?", "received"),
        ("Bora! Que tal domingo?", "sent"),
        ("Domingo tá ótimo. Meio-dia?", "received"),
        ("Fechado! Te vejo lá", "sent"),
    ],
    [
        ("Oi! Tudo bem?", "received"),
        ("Tudo sim, e você?", "sent"),
        ("Tudo ótimo! Te mandei aquele documento por email", "received"),
        ("Vi aqui, obrigado!", "sent"),
    ],
    [
        ("Você viu o jogo ontem?", "received"),
        ("Vi! Que partida incrível", "sent"),
        ("Pois é! Aquele gol no final foi sensacional", "received"),
    ],
    [
        ("Preciso de um favor", "received"),
        ("Claro, pode falar", "sent"),
        ("Consegue buscar aquele documento pra mim amanhã?", "received"),
        ("Consigo sim, sem problemas", "sent"),
    ],
    [
        ("Chegou bem em casa?", "received"),
        ("Cheguei sim, obrigado!", "sent"),
        ("Ótimo! Foi muito bom te ver", "received"),
        ("Também adorei! Vamos repetir em breve", "sent"),
    ],
    [
        ("Desculpa a demora pra responder", "sent"),
        ("Sem problema! Tava ocupado?", "received"),
        ("Sim, reunião que não acabava nunca", "sent"),
    ],
    [
        ("Você recomenda aquele restaurante?", "received"),
        ("Recomendo muito! Comida excelente", "sent"),
        ("Vou marcar pra semana que vem então", "received"),
        ("Vai gostar com certeza!", "sent"),
    ],
    [
        ("Bom dia! Como foi o final de semana?", "received"),
        ("Foi ótimo! Descansamos bastante", "sent"),
        ("Que bom! Merecido", "received"),
    ],
    [
        ("Oi! Você tá aí?", "received"),
        ("To sim, pode falar", "sent"),
        ("Esqueci de te passar uma informação importante", "received"),
        ("Qual?", "sent"),
    ],
]

def generate_avatar_color() -> str:
    """
    Gera uma cor aleatória para o avatar das redes sociais.

    Esta função seleciona uma cor hexadecimal aleatória de uma lista predefinida
    que contém cores modernas e vibrantes comumente usadas em interfaces de
    redes sociais para avatares de usuários.

    Returns:
        str: Código de cor hexadecimal (ex: '#1DA1F2', '#E1306C')

    Exemplo:
        >>> color = generate_avatar_color()
        >>> print(color)
        '#8B5CF6'
    """
    colors = [
        '#1DA1F2', '#E1306C', '#25D366', '#FF6900', '#8B5CF6',
        '#EC4899', '#10B981', '#F59E0B', '#6366F1', '#EF4444',
        '#06B6D4', '#84CC16', '#F97316', '#A855F7', '#14B8A6'
    ]
    return random.choice(colors)


def get_initials(name: str) -> str:
    """
    Extrai as iniciais de um nome completo para usar em avatares.

    Esta função processa um nome completo e retorna as primeiras letras
    dos dois primeiros nomes em maiúsculo. É útil para criar avatares
    com texto quando não há imagem de perfil disponível.

    Args:
        name (str): Nome completo do usuário

    Returns:
        str: Iniciais em maiúsculo (ex: 'JD' para 'João da Silva')
             Se o nome tiver apenas uma palavra, retorna a primeira letra
             Se o nome estiver vazio, retorna '?'

    Exemplo:
        >>> get_initials('Maria Santos')
        'MS'
        >>> get_initials('João')
        'J'
        >>> get_initials('')
        '?'
    """
    parts = name.split()
    if len(parts) >= 2:
        return f"{parts[0][0]}{parts[1][0]}".upper()
    return name[0].upper() if name else "?"


def generate_username(name: str) -> str:
    """
    Gera um nome de usuário (username) realista baseado no nome real.

    Esta função cria usernames que simulam os padrões comuns das redes sociais:
    - Remove espaços e converte para minúsculo
    - Adiciona sufixos aleatórios como números ou texto
    - Inclui o símbolo '@' no início

    Args:
        name (str): Nome real do usuário

    Returns:
        str: Username gerado com '@' (ex: '@joaosilva123', '@maria_oficial')

    Exemplo:
        >>> generate_username('João Silva')
        '@joaosilva_real'
        >>> generate_username('Maria Santos')
        '@mariasantosbr'
    """
    name_parts = name.lower().replace(' ', '')
    number = random.randint(1, 999)
    suffixes = ['_oficial', '_real', 'br', str(number), f'{number}']
    return f"@{name_parts}{random.choice(suffixes)}"


def generate_tweet_text() -> str:
    """
    Seleciona aleatoriamente um texto de tweet realista.

    Esta função escolhe um tweet da lista predefinida REAL_TWEETS,
    que contém textos autênticos e variados que simulam conversas
    reais do Twitter brasileiro, incluindo diversos temas como:
    - Cotidiano e reflexões pessoais
    - Comentários sobre política e sociedade
    - Experiências do dia a dia
    - Opiniões sobre entretenimento

    Returns:
        str: Texto de tweet realista em português

    Exemplo:
        >>> tweet = generate_tweet_text()
        >>> print(tweet)
        'Acabei de assistir esse filme e não consigo parar de pensar nele.'
    """
    return random.choice(REAL_TWEETS)


def generate_instagram_caption() -> str:
    """
    Seleciona aleatoriamente uma legenda (caption) realista para Instagram.

    Esta função escolhe uma caption da lista REAL_CAPTIONS, que contém
    legendas típicas do Instagram brasileiro com características como:
    - Frases inspiracionais e motivacionais
    - Reflexões sobre momentos do dia
    - Uso de emojis apropriados
    - Tom positivo e pessoal
    - Linguagem casual e acessível

    Returns:
        str: Caption realista com emojis incluídos

    Exemplo:
        >>> caption = generate_instagram_caption()
        >>> print(caption)
        'Momentos simples são os melhores ☀️'
    """
    return random.choice(REAL_CAPTIONS)


def generate_whatsapp_messages() -> List[Tuple[str, str]]:
    """
    Seleciona uma conversa realista do WhatsApp da lista predefinida.

    Esta função retorna uma sequência de mensagens que simula uma conversa
    natural entre duas pessoas, incluindo:
    - Diálogos cotidianos e naturais
    - Alternância entre mensagens enviadas e recebidas
    - Contextos variados (trabalho, amizade, família)
    - Linguagem informal típica do WhatsApp

    Returns:
        List[Tuple[str, str]]: Lista de tuplas onde cada tupla contém:
            - str: Texto da mensagem
            - str: Tipo da mensagem ('sent' ou 'received')

    Exemplo:
        >>> conversa = generate_whatsapp_messages()
        >>> print(conversa)
        [('E aí, conseguiu resolver aquele problema?', 'received'),
         ('Consegui sim! Deu tudo certo no final', 'sent')]
    """
    return random.choice(REAL_CONVERSATIONS)


def format_number(num: int) -> str:
    """
    Formata números grandes para exibição compacta nas redes sociais.

    Esta função converte números inteiros para o formato abreviado
    usado nas redes sociais, facilitando a leitura de métricas como
    curtidas, visualizações e compartilhamentos.

    Regras de formatação:
    - Números >= 1.000.000: formato 'X.XM' (milhões)
    - Números >= 1.000: formato 'X.XK' (milhares)
    - Números < 1.000: exibição normal

    Args:
        num (int): Número inteiro a ser formatado

    Returns:
        str: Número formatado com sufixo apropriado

    Exemplo:
        >>> format_number(1500)
        '1.5K'
        >>> format_number(2500000)
        '2.5M'
        >>> format_number(999)
        '999'
    """
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)


def generate_timestamp(days_ago: int = None) -> str:
    """
    Gera um timestamp relativo realista para posts de redes sociais.

    Esta função cria timestamps que simulam como as redes sociais
    exibem o tempo de publicação de posts, usando formatos relativos
    para datas recentes e formato absoluto para datas mais antigas.

    Formatos gerados:
    - Posts do mesmo dia: 'Xh' (horas atrás)
    - Posts de ontem: '1d'
    - Posts da semana: 'Xd' (dias atrás)
    - Posts mais antigos: 'DD/MM/AAAA'

    Args:
        days_ago (int, optional): Número específico de dias atrás.
                                 Se None, será gerado aleatoriamente (0-7 dias)

    Returns:
        str: Timestamp formatado

    Exemplo:
        >>> generate_timestamp(0)
        '5h'
        >>> generate_timestamp(1)
        '1d'
        >>> generate_timestamp(15)
        '04/10/2024'
    """
    if days_ago is None:
        days_ago = random.randint(0, 7)

    if days_ago == 0:
        hours = random.randint(1, 23)
        return f"{hours}h"
    elif days_ago == 1:
        return "1d"
    elif days_ago <= 7:
        return f"{days_ago}d"
    else:
        date = datetime.now() - timedelta(days=days_ago)
        return date.strftime("%d/%m/%Y")


def generate_time() -> str:
    """
    Gera um horário aleatório para mensagens do WhatsApp.

    Esta função cria horários no formato HH:MM que são exibidos
    nas mensagens do WhatsApp. O horário é gerado aleatoriamente
    dentro de um dia completo (00:00 a 23:59).

    Returns:
        str: Horário no formato 'HH:MM' com zero à esquerda quando necessário

    Exemplo:
        >>> time = generate_time()
        >>> print(time)
        '14:30'
        >>> print(generate_time())
        '09:05'
    """
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    return f"{hour:02d}:{minute:02d}"


# ============================================================================
# FUNÇÕES DE SCREENSHOT
# ============================================================================

async def create_twitter_screenshot(page: Page, filename: str) -> Dict:
    """
    Cria um screenshot autêntico de um post do Twitter.

    Esta função assíncrona gera uma imagem de um tweet realista usando
    o template HTML do Twitter. Ela cria dados fictícios mas verossímeis
    para todos os elementos do post e renderiza usando Playwright.

    Elementos gerados:
    - Perfil do usuário (nome, username, avatar, verificação)
    - Conteúdo do tweet
    - Métricas de engajamento (curtidas, retweets, visualizações)
    - Timestamp realista

    Args:
        page (Page): Instância da página do Playwright para renderização
        filename (str): Caminho onde salvar o screenshot

    Returns:
        Dict: Dicionário com todos os dados gerados para o tweet,
              usado posteriormente para criar versões manipuladas

    Exemplo:
        async def exemplo():
            data = await create_twitter_screenshot(page, 'tweet_001.png')
            print(data['name'])  # 'João Silva'
            print(data['like_count'])  # 5420
    """

    # Dados fictícios
    name = fake.name()
    username = generate_username(name)
    text = generate_tweet_text()
    verified = random.random() < 0.3  # 30% de chance de ser verificado

    reply_count = random.randint(5, 500)
    retweet_count = random.randint(10, 2000)
    quote_count = random.randint(5, 800)
    like_count = random.randint(50, 10000)
    view_count = random.randint(1000, 100000)

    timestamp = generate_timestamp()
    avatar_color = generate_avatar_color()
    initials = get_initials(name)

    # Carregar template
    template_path = TEMPLATES_DIR / "twitter.html"
    await page.goto(f"file:///{template_path.absolute()}")

    # Preencher dados
    await page.evaluate(f"""
        document.getElementById('avatar').textContent = '{initials}';
        document.getElementById('avatar').style.backgroundColor = '{avatar_color}';
        document.getElementById('displayName').textContent = '{name}';
        document.getElementById('username').textContent = '{username}';
        document.getElementById('timestamp').textContent = '{timestamp}';
        document.getElementById('tweetText').textContent = '{text}';
        document.getElementById('retweetCount').textContent = '{format_number(retweet_count)}';
        document.getElementById('quoteCount').textContent = '{format_number(quote_count)}';
        document.getElementById('likeCount').textContent = '{format_number(like_count)}';
        document.getElementById('viewCount').textContent = '{format_number(view_count)}';
        document.getElementById('replyCount').textContent = '{format_number(reply_count)}';
        document.getElementById('retweetActionCount').textContent = '{format_number(retweet_count)}';
        document.getElementById('likeActionCount').textContent = '{format_number(like_count)}';
        document.getElementById('viewActionCount').textContent = '{format_number(view_count)}';
        document.getElementById('verifiedBadge').style.display = '{' inline-flex' if verified else 'none'}';
    """)

    # Screenshot
    await page.screenshot(path=filename)

    # Retornar dados para manipulação posterior
    return {
        'name': name,
        'username': username,
        'text': text,
        'verified': verified,
        'reply_count': reply_count,
        'retweet_count': retweet_count,
        'quote_count': quote_count,
        'like_count': like_count,
        'view_count': view_count,
        'timestamp': timestamp,
        'avatar_color': avatar_color,
        'initials': initials,
    }


async def create_instagram_screenshot(page: Page, filename: str) -> Dict:
    """
    Cria um screenshot autêntico de um post do Instagram.

    Esta função assíncrona gera uma imagem de um post realista do Instagram
    usando o template HTML correspondente. Simula a aparência típica de
    posts da rede social com todos os elementos visuais.

    Elementos gerados:
    - Perfil do usuário (nome, username, avatar, badge de verificação)
    - Caption/legenda do post
    - Métricas (curtidas, comentários)
    - Timestamp e elementos de interface

    Args:
        page (Page): Instância da página do Playwright para renderização
        filename (str): Caminho onde salvar o screenshot

    Returns:
        Dict: Dicionário com todos os dados gerados para o post,
              usado posteriormente para criar versões manipuladas

    Exemplo:
        async def exemplo():
            data = await create_instagram_screenshot(page, 'insta_001.png')
            print(data['username'])  # 'maria_santos123'
            print(data['like_count'])  # 1250
    """

    # Dados fictícios
    name = fake.name()
    username = generate_username(name).replace('@', '')
    caption = generate_instagram_caption()
    verified = random.random() < 0.2  # 20% de chance de ser verificado

    like_count = random.randint(50, 50000)
    comment_count = random.randint(5, 1000)

    timestamp = generate_timestamp()
    avatar_color = generate_avatar_color()
    initials = get_initials(name)

    # Carregar template
    template_path = TEMPLATES_DIR / "instagram.html"
    await page.goto(f"file:///{template_path.absolute()}")

    # Preencher dados
    comments_text = f"Ver todos os {comment_count} comentários" if comment_count > 1 else "Ver comentário"

    await page.evaluate(f"""
        document.getElementById('avatar').textContent = '{initials}';
        document.getElementById('avatar').style.backgroundColor = '{avatar_color}';
        document.getElementById('username').textContent = '{username}';
        document.getElementById('captionUsername').textContent = '{username}';
        document.getElementById('captionText').textContent = '{caption}';
        document.getElementById('likeCount').textContent = '{format_number(like_count)}';
        document.getElementById('viewComments').textContent = '{comments_text}';
        document.getElementById('timestamp').textContent = '{timestamp}';
        document.getElementById('verifiedBadge').style.display = '{"inline-flex" if verified else "none"}';
    """)

    # Screenshot
    await page.screenshot(path=filename)

    return {
        'name': name,
        'username': username,
        'caption': caption,
        'verified': verified,
        'like_count': like_count,
        'comment_count': comment_count,
        'timestamp': timestamp,
        'avatar_color': avatar_color,
        'initials': initials,
    }


async def create_whatsapp_screenshot(page: Page, filename: str) -> Dict:
    """
    Cria um screenshot autêntico de uma conversa do WhatsApp.

    Esta função assíncrona gera uma imagem de uma conversa realista
    do WhatsApp usando o template HTML correspondente. Simula a interface
    típica da aplicação com múltiplas mensagens em uma conversa.

    Elementos gerados:
    - Cabeçalho com nome e avatar do contato
    - Sequência de mensagens (enviadas e recebidas)
    - Horários individuais para cada mensagem
    - Badge de data da conversa
    - Layout autêntico da interface do WhatsApp

    Args:
        page (Page): Instância da página do Playwright para renderização
        filename (str): Caminho onde salvar o screenshot

    Returns:
        Dict: Dicionário com todos os dados gerados para a conversa,
              usado posteriormente para criar versões manipuladas

    Exemplo:
        async def exemplo():
            data = await create_whatsapp_screenshot(page, 'whats_001.png')
            print(data['contact_name'])  # 'Ana Costa'
            print(len(data['messages']))  # 4
    """

    # Dados fictícios
    contact_name = fake.name()
    messages = generate_whatsapp_messages()
    date_badge = generate_timestamp(random.randint(0, 3))

    avatar_color = generate_avatar_color()
    initials = get_initials(contact_name)

    # Carregar template
    template_path = TEMPLATES_DIR / "whatsapp.html"
    await page.goto(f"file:///{template_path.absolute()}")

    # Preencher dados do contato
    await page.evaluate(f"""
        document.getElementById('avatar').textContent = '{initials}';
        document.getElementById('avatar').style.backgroundColor = '{avatar_color}';
        document.getElementById('contactName').textContent = '{contact_name}';
        document.getElementById('dateBadge').textContent = '{date_badge}';
    """)

    # Adicionar mensagens
    for msg_text, msg_type in messages:
        time = generate_time()
        escaped_text = msg_text.replace("'", "\\'").replace('"', '\\"')
        await page.evaluate(f"""
            const container = document.getElementById('messagesContainer');
            const msg = createMessage('{escaped_text}', '{time}', '{msg_type}');
            container.appendChild(msg);
        """)

    # Screenshot
    await page.screenshot(path=filename)

    return {
        'contact_name': contact_name,
        'messages': messages,
        'date_badge': date_badge,
        'avatar_color': avatar_color,
        'initials': initials,
    }


# ============================================================================
# FUNÇÕES DE MANIPULAÇÃO
# ============================================================================

async def manipulate_twitter(page: Page, original_data: Dict, manipulation_type: str) -> Dict:
    """
    Aplica manipulações específicas em um post autêntico do Twitter.

    Esta função cria versões manipuladas de tweets originais para treinar
    modelos de detecção de conteúdo falso. As manipulações simulam alterações
    comuns feitas em screenshots para desinformação ou fraude.

    Tipos de manipulação disponíveis:
    - 'metrics_change': Altera números de curtidas, retweets e visualizações
    - 'text_change': Substitui o texto do tweet por outro conteúdo
    - 'verification_change': Adiciona/remove o selo de verificação
    - 'username_change': Modifica ligeiramente o username
    - 'combined': Combina múltiplas alterações simultaneamente

    Args:
        page (Page): Instância da página do Playwright para renderização
        original_data (Dict): Dados originais do tweet autêntico
        manipulation_type (str): Tipo de manipulação a ser aplicada

    Returns:
        Dict: Dados modificados após aplicação da manipulação

    Exemplo:
        async def exemplo():
            manipulated = await manipulate_twitter(page, original, 'metrics_change')
            # Métricas alteradas em ±20-50% dos valores originais
    """

    data = original_data.copy()

    if manipulation_type == "metrics_change":
        # Alterar métricas (±20-50%)
        factor = random.uniform(0.5, 1.5)
        data['like_count'] = int(data['like_count'] * factor)
        data['retweet_count'] = int(data['retweet_count'] * factor)
        data['view_count'] = int(data['view_count'] * factor)

    elif manipulation_type == "text_change":
        # Garantir que o texto seja diferente do original
        new_text = generate_tweet_text()
        while new_text == original_data['text']:
            new_text = generate_tweet_text()
        data['text'] = new_text

    elif manipulation_type == "verification_change":
        # Inverter status de verificação
        data['verified'] = not data['verified']

    elif manipulation_type == "username_change":
        # Alterar username levemente
        data['username'] = generate_username(data['name'])

    elif manipulation_type == "combined":
        # Combinação de alterações
        factor = random.uniform(0.7, 1.3)
        data['like_count'] = int(data['like_count'] * factor)
        data['verified'] = not data['verified']

    # Carregar template e aplicar dados manipulados
    template_path = TEMPLATES_DIR / "twitter.html"
    await page.goto(f"file:///{template_path.absolute()}")

    await page.evaluate(f"""
        document.getElementById('avatar').textContent = '{data['initials']}';
        document.getElementById('avatar').style.backgroundColor = '{data['avatar_color']}';
        document.getElementById('displayName').textContent = '{data['name']}';
        document.getElementById('username').textContent = '{data['username']}';
        document.getElementById('timestamp').textContent = '{data['timestamp']}';
        document.getElementById('tweetText').textContent = '{data['text']}';
        document.getElementById('retweetCount').textContent = '{format_number(data['retweet_count'])}';
        document.getElementById('quoteCount').textContent = '{format_number(data['quote_count'])}';
        document.getElementById('likeCount').textContent = '{format_number(data['like_count'])}';
        document.getElementById('viewCount').textContent = '{format_number(data['view_count'])}';
        document.getElementById('replyCount').textContent = '{format_number(data['reply_count'])}';
        document.getElementById('retweetActionCount').textContent = '{format_number(data['retweet_count'])}';
        document.getElementById('likeActionCount').textContent = '{format_number(data['like_count'])}';
        document.getElementById('viewActionCount').textContent = '{format_number(data['view_count'])}';
        document.getElementById('verifiedBadge').style.display = '{"inline-flex" if data['verified'] else "none"}';
    """)

    return data


async def manipulate_instagram(page: Page, original_data: Dict, manipulation_type: str) -> Dict:
    """
    Aplica manipulações específicas em um post autêntico do Instagram.

    Esta função cria versões manipuladas de posts originais do Instagram
    para dataset de treinamento de detecção de conteúdo manipulado.
    As alterações simulam modificações típicas em screenshots fraudulentos.

    Tipos de manipulação disponíveis:
    - 'metrics_change': Altera apenas o número de curtidas
    - 'caption_change': Substitui a legenda por outra diferente
    - 'verification_change': Adiciona/remove o badge de verificação
    - 'username_change': Modifica o username do perfil
    - 'combined': Aplica múltiplas alterações em conjunto

    Args:
        page (Page): Instância da página do Playwright para renderização
        original_data (Dict): Dados originais do post autêntico
        manipulation_type (str): Tipo de manipulação a ser aplicada

    Returns:
        Dict: Dados modificados após aplicação da manipulação

    Exemplo:
        async def exemplo():
            manipulated = await manipulate_instagram(page, original, 'caption_change')
            # Caption foi substituída por uma diferente da lista
    """

    data = original_data.copy()

    if manipulation_type == "metrics_change":
        factor = random.uniform(0.5, 1.5)
        data['like_count'] = int(data['like_count'] * factor)

    elif manipulation_type == "caption_change":
        # Garantir que a caption seja diferente da original
        new_caption = generate_instagram_caption()
        while new_caption == original_data['caption']:
            new_caption = generate_instagram_caption()
        data['caption'] = new_caption

    elif manipulation_type == "verification_change":
        data['verified'] = not data['verified']

    elif manipulation_type == "username_change":
        data['username'] = generate_username(data['name']).replace('@', '')

    elif manipulation_type == "combined":
        factor = random.uniform(0.7, 1.3)
        data['like_count'] = int(data['like_count'] * factor)
        # Garantir que a caption seja diferente da original
        new_caption = generate_instagram_caption()
        while new_caption == original_data['caption']:
            new_caption = generate_instagram_caption()
        data['caption'] = new_caption

    # Carregar template e aplicar dados manipulados
    template_path = TEMPLATES_DIR / "instagram.html"
    await page.goto(f"file:///{template_path.absolute()}")

    comments_text = f"Ver todos os {data['comment_count']} comentários" if data['comment_count'] > 1 else "Ver comentário"

    await page.evaluate(f"""
        document.getElementById('avatar').textContent = '{data['initials']}';
        document.getElementById('avatar').style.backgroundColor = '{data['avatar_color']}';
        document.getElementById('username').textContent = '{data['username']}';
        document.getElementById('captionUsername').textContent = '{data['username']}';
        document.getElementById('captionText').textContent = '{data['caption']}';
        document.getElementById('likeCount').textContent = '{format_number(data['like_count'])}';
        document.getElementById('viewComments').textContent = '{comments_text}';
        document.getElementById('timestamp').textContent = '{data['timestamp']}';
        document.getElementById('verifiedBadge').style.display = '{"inline-flex" if data['verified'] else "none"}';
    """)

    return data


async def manipulate_whatsapp(page: Page, original_data: Dict, manipulation_type: str) -> Dict:
    """
    Aplica manipulações específicas em uma conversa autêntica do WhatsApp.

    Esta função cria versões manipuladas de conversas originais do WhatsApp
    para treinar modelos de detecção de screenshots alterados. As modificações
    simulam alterações comuns em conversas falsificadas.

    Tipos de manipulação disponíveis:
    - 'message_change': Substitui toda a conversa por mensagens diferentes
    - 'contact_change': Altera o nome do contato no cabeçalho
    - 'time_change': Mensagens recebem novos horários na recriação
    - 'combined': Combina alteração de contato e mensagens

    Args:
        page (Page): Instância da página do Playwright para renderização
        original_data (Dict): Dados originais da conversa autêntica
        manipulation_type (str): Tipo de manipulação a ser aplicada

    Returns:
        Dict: Dados modificados após aplicação da manipulação

    Exemplo:
        async def exemplo():
            manipulated = await manipulate_whatsapp(page, original, 'contact_change')
            print(manipulated['contact_name'])  # 'Pedro Lima' (nome diferente do original)
    """

    data = original_data.copy()

    if manipulation_type == "message_change":
        # Garantir que as mensagens sejam diferentes das originais
        new_messages = generate_whatsapp_messages()
        while new_messages == original_data['messages']:
            new_messages = generate_whatsapp_messages()
        data['messages'] = new_messages

    elif manipulation_type == "contact_change":
        # Alterar nome do contato
        data['contact_name'] = fake.name()
        data['initials'] = get_initials(data['contact_name'])

    elif manipulation_type == "time_change":
        # Os horários são automaticamente regenerados quando as mensagens são recriadas
        # Cada mensagem receberá um novo horário aleatório via generate_time()
        pass

    elif manipulation_type == "combined":
        data['contact_name'] = fake.name()
        data['initials'] = get_initials(data['contact_name'])
        # Garantir que as mensagens sejam diferentes das originais
        new_messages = generate_whatsapp_messages()
        while new_messages == original_data['messages']:
            new_messages = generate_whatsapp_messages()
        data['messages'] = new_messages

    # Carregar template e aplicar dados manipulados
    template_path = TEMPLATES_DIR / "whatsapp.html"
    await page.goto(f"file:///{template_path.absolute()}")

    await page.evaluate(f"""
        document.getElementById('avatar').textContent = '{data['initials']}';
        document.getElementById('avatar').style.backgroundColor = '{data['avatar_color']}';
        document.getElementById('contactName').textContent = '{data['contact_name']}';
        document.getElementById('dateBadge').textContent = '{data['date_badge']}';
    """)

    # Adicionar mensagens
    for msg_text, msg_type in data['messages']:
        time = generate_time()
        escaped_text = msg_text.replace("'", "\\'").replace('"', '\\"')
        await page.evaluate(f"""
            const container = document.getElementById('messagesContainer');
            const msg = createMessage('{escaped_text}', '{time}', '{msg_type}');
            container.appendChild(msg);
        """)

    return data


# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

async def generate_dataset():
    """
    Função principal que orquestra a geração completa do dataset.

    Esta função assíncrona coordena todo o processo de criação do dataset
    de screenshots de redes sociais, incluindo:

    Processo de geração:
    1. Inicializa o browser Playwright para renderização
    2. Para cada plataforma (Twitter, Instagram, WhatsApp):
       - Cria screenshots autênticos usando templates HTML
       - Gera múltiplas versões manipuladas de cada screenshot
       - Salva metadados para labels do dataset
    3. Exporta arquivo CSV com labels para treinamento ML

    Estrutura do dataset gerado:
    - Pasta 'autenticos/': Screenshots originais não modificados
    - Pasta 'manipulados/': Versões alteradas dos originais
    - Arquivo 'labels.csv': Metadados e labels para cada imagem

    Configurações (definidas nas constantes):
    - POSTS_PER_PLATFORM: Quantos posts criar por rede social
    - MANIPULATIONS_PER_POST: Quantas versões manipuladas por post

    Raises:
        Exception: Qualquer erro na geração dos screenshots ou templates

    Exemplo de uso:
        async def main():
            await generate_dataset()
            # Output:
            # >> Iniciando geracao do dataset...
            # >> Serao gerados: 60 autenticos + 180 manipulados
            # [SUCESSO] Dataset gerado com sucesso!
    """

    print(">> Iniciando geracao do dataset...")
    print(f">> Serao gerados: {POSTS_PER_PLATFORM * 3} autenticos + {POSTS_PER_PLATFORM * 3 * MANIPULATIONS_PER_POST} manipulados")
    print(f">> Total: {POSTS_PER_PLATFORM * 3 * (1 + MANIPULATIONS_PER_POST)} imagens\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 600, 'height': 800})

        platforms = [
            ('twitter', create_twitter_screenshot, manipulate_twitter),
            ('instagram', create_instagram_screenshot, manipulate_instagram),
            ('whatsapp', create_whatsapp_screenshot, manipulate_whatsapp),
        ]

        for platform_name, create_func, manipulate_func in platforms:
            print(f">> Gerando {platform_name.upper()}...")

            for i in range(POSTS_PER_PLATFORM):
                # Criar screenshot autêntico
                authentic_filename = AUTHENTIC_DIR / f"{platform_name}_{i:03d}.png"
                original_data = await create_func(page, str(authentic_filename))

                # Adicionar metadados
                dataset_metadata.append({
                    'filename': authentic_filename.name,
                    'class': 'autentico',
                    'manipulation_type': 'none',
                    'original_filename': authentic_filename.name,
                    'social_network': platform_name
                })

                print(f"  [OK] {authentic_filename.name}")

                # Criar manipulações
                if platform_name == "twitter":
                    manipulation_types = [
                        "metrics_change",
                        "text_change",
                        "verification_change",
                    ]
                elif platform_name == "instagram":
                    manipulation_types = [
                        "metrics_change",
                        "caption_change",
                        "verification_change",
                    ]
                elif platform_name == "whatsapp":
                    manipulation_types = [
                        "time_change",
                        "message_change",
                        "contact_change",
                    ]

                for j, manip_type in enumerate(manipulation_types):
                    manipulated_filename = MANIPULATED_DIR / f"{platform_name}_{i:03d}_manip_{j+1}.png"

                    await manipulate_func(page, original_data, manip_type)
                    await page.screenshot(path=str(manipulated_filename))

                    dataset_metadata.append({
                        'filename': manipulated_filename.name,
                        'class': 'manipulado',
                        'manipulation_type': manip_type,
                        'original_filename': authentic_filename.name,
                        'social_network': platform_name
                    })

                    print(f"    -> {manipulated_filename.name} ({manip_type})")

            print()

        await browser.close()

    # Salvar metadados em CSV
    df = pd.DataFrame(dataset_metadata)
    csv_path = DATASET_DIR / "labels.csv"
    df.to_csv(csv_path, index=False, encoding='utf-8')

    print("\n[SUCESSO] Dataset gerado com sucesso!")
    print(f"\n>> Estatisticas:")
    print(f"   - Total de imagens: {len(dataset_metadata)}")
    print(f"   - Autenticos: {len(df[df['class'] == 'autentico'])}")
    print(f"   - Manipulados: {len(df[df['class'] == 'manipulado'])}")
    print(f"\n>> Arquivos salvos em:")
    print(f"   - {AUTHENTIC_DIR}")
    print(f"   - {MANIPULATED_DIR}")
    print(f"   - {csv_path}")


if __name__ == "__main__":
    asyncio.run(generate_dataset())
