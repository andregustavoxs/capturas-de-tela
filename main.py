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
    """Gera uma cor aleatória para o avatar"""
    colors = [
        '#1DA1F2', '#E1306C', '#25D366', '#FF6900', '#8B5CF6',
        '#EC4899', '#10B981', '#F59E0B', '#6366F1', '#EF4444',
        '#06B6D4', '#84CC16', '#F97316', '#A855F7', '#14B8A6'
    ]
    return random.choice(colors)


def get_initials(name: str) -> str:
    """Retorna as iniciais de um nome"""
    parts = name.split()
    if len(parts) >= 2:
        return f"{parts[0][0]}{parts[1][0]}".upper()
    return name[0].upper() if name else "?"


def generate_username(name: str) -> str:
    """Gera um username baseado no nome"""
    name_parts = name.lower().replace(' ', '')
    number = random.randint(1, 999)
    suffixes = ['_oficial', '_real', 'br', str(number), f'{number}']
    return f"@{name_parts}{random.choice(suffixes)}"


def generate_tweet_text() -> str:
    """Retorna um tweet realista da lista"""
    return random.choice(REAL_TWEETS)


def generate_instagram_caption() -> str:
    """Retorna uma caption realista da lista"""
    return random.choice(REAL_CAPTIONS)


def generate_whatsapp_messages() -> List[Tuple[str, str]]:
    """Retorna uma conversa realista da lista"""
    return random.choice(REAL_CONVERSATIONS)


def format_number(num: int) -> str:
    """Formata números para display (1.2K, 5.3M, etc)"""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)


def generate_timestamp(days_ago: int = None) -> str:
    """Gera timestamp relativo"""
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
    """Gera horário para mensagens do WhatsApp"""
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    return f"{hour:02d}:{minute:02d}"


# ============================================================================
# FUNÇÕES DE SCREENSHOT
# ============================================================================

async def create_twitter_screenshot(page: Page, filename: str) -> Dict:
    """Cria screenshot de um post do Twitter"""

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
    """Cria screenshot de um post do Instagram"""

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
    """Cria screenshot de uma conversa do WhatsApp"""

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
    """Aplica manipulação em um post do Twitter"""

    data = original_data.copy()

    if manipulation_type == "metrics_change":
        # Alterar métricas (±20-50%)
        factor = random.uniform(0.5, 1.5)
        data['like_count'] = int(data['like_count'] * factor)
        data['retweet_count'] = int(data['retweet_count'] * factor)
        data['view_count'] = int(data['view_count'] * factor)

    elif manipulation_type == "text_change":
        # Alterar texto
        data['text'] = generate_tweet_text()

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
    """Aplica manipulação em um post do Instagram"""

    data = original_data.copy()

    if manipulation_type == "metrics_change":
        factor = random.uniform(0.5, 1.5)
        data['like_count'] = int(data['like_count'] * factor)

    elif manipulation_type == "caption_change":
        data['caption'] = generate_instagram_caption()

    elif manipulation_type == "verification_change":
        data['verified'] = not data['verified']

    elif manipulation_type == "username_change":
        data['username'] = generate_username(data['name']).replace('@', '')

    elif manipulation_type == "combined":
        factor = random.uniform(0.7, 1.3)
        data['like_count'] = int(data['like_count'] * factor)
        data['caption'] = generate_instagram_caption()

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
    """Aplica manipulação em uma conversa do WhatsApp"""

    data = original_data.copy()

    if manipulation_type == "message_change":
        # Alterar texto de uma mensagem
        data['messages'] = generate_whatsapp_messages()

    elif manipulation_type == "contact_change":
        # Alterar nome do contato
        data['contact_name'] = fake.name()
        data['initials'] = get_initials(data['contact_name'])

    elif manipulation_type == "time_change":
        # As mensagens terão novos horários quando recriadas
        pass

    elif manipulation_type == "combined":
        data['contact_name'] = fake.name()
        data['initials'] = get_initials(data['contact_name'])
        data['messages'] = generate_whatsapp_messages()

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
    """Gera todo o dataset de screenshots"""

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
                manipulation_types = [
                    "metrics_change",
                    "text_change" if platform_name != "whatsapp" else "message_change",
                    "verification_change" if platform_name != "whatsapp" else "contact_change",
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
