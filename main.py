"""
Gerador de Dataset de Screenshots de Redes Sociais
Cria screenshots autênticos e manipulados para treinamento de modelos ML
"""

import asyncio
import pandas as pd
from playwright.async_api import async_playwright

from src.config import (
    POSTS_PER_PLATFORM,
    MANIPULATIONS_PER_POST,
    AUTHENTIC_DIR,
    MANIPULATED_DIR,
    DATASET_DIR
)
from src.screenshots import (
    create_twitter_screenshot,
    create_instagram_screenshot,
    create_whatsapp_screenshot
)
from src.manipulations import (
    manipulate_twitter,
    manipulate_instagram,
    manipulate_whatsapp
)


# Lista para armazenar metadados
dataset_metadata = []


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
