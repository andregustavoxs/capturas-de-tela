"""
Funções para manipulação de screenshots de redes sociais
"""

import random
from typing import Dict
from playwright.async_api import Page
from .config import fake, TEMPLATES_DIR
from .generators import (
    get_initials,
    generate_username,
    generate_tweet_text,
    generate_instagram_caption,
    generate_whatsapp_messages,
    format_number,
    generate_time
)


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
