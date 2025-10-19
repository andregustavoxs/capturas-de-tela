"""
Funções geradoras de dados fictícios para redes sociais
"""

import random
from datetime import datetime, timedelta
from typing import List, Tuple
from .config import (
    fake,
    REAL_TWEETS,
    REAL_CAPTIONS,
    REAL_CONVERSATIONS,
    AVATAR_COLORS
)


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
    return random.choice(AVATAR_COLORS)


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
