"""
Funções para criação de screenshots de redes sociais
"""

import random
from typing import Dict
from playwright.async_api import Page
from .config import fake, TEMPLATES_DIR
from .generators import (
    generate_avatar_color,
    get_initials,
    generate_username,
    generate_tweet_text,
    generate_instagram_caption,
    generate_whatsapp_messages,
    format_number,
    generate_timestamp,
    generate_time
)


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
