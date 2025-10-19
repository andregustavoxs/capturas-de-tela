"""
Dataset Generator - Gerador de Screenshots de Redes Sociais
Módulo para criação de datasets de screenshots autênticos e manipulados
"""

__version__ = "1.0.0"
__author__ = "André Gustavo"

from .config import (
    POSTS_PER_PLATFORM,
    MANIPULATIONS_PER_POST,
    AUTHENTIC_DIR,
    MANIPULATED_DIR,
    DATASET_DIR,
    fake
)

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

from .screenshots import (
    create_twitter_screenshot,
    create_instagram_screenshot,
    create_whatsapp_screenshot
)

from .manipulations import (
    manipulate_twitter,
    manipulate_instagram,
    manipulate_whatsapp
)

__all__ = [
    # Config
    'POSTS_PER_PLATFORM',
    'MANIPULATIONS_PER_POST',
    'AUTHENTIC_DIR',
    'MANIPULATED_DIR',
    'DATASET_DIR',
    'fake',
    # Generators
    'generate_avatar_color',
    'get_initials',
    'generate_username',
    'generate_tweet_text',
    'generate_instagram_caption',
    'generate_whatsapp_messages',
    'format_number',
    'generate_timestamp',
    'generate_time',
    # Screenshots
    'create_twitter_screenshot',
    'create_instagram_screenshot',
    'create_whatsapp_screenshot',
    # Manipulations
    'manipulate_twitter',
    'manipulate_instagram',
    'manipulate_whatsapp',
]
