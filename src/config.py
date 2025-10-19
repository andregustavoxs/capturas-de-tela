"""
Configurações e constantes do gerador de dataset
"""

import random
from pathlib import Path
from faker import Faker

# Configurações de seed para reprodutibilidade
SEED = 42
random.seed(SEED)
Faker.seed(SEED)

# Inicializar Faker com locale brasileiro
fake = Faker('pt_BR')

# Diretórios
# config.py está em src/
PROJECT_ROOT = Path(__file__).parent.parent  # Raiz do projeto
SRC_DIR = Path(__file__).parent  # Pasta src/

TEMPLATES_DIR = PROJECT_ROOT / "templates"  # Templates na raiz
DATASET_DIR = SRC_DIR / "dataset"  # Dataset dentro de src/
AUTHENTIC_DIR = DATASET_DIR / "autenticos"
MANIPULATED_DIR = DATASET_DIR / "manipulados"

# Criar diretórios se não existirem
AUTHENTIC_DIR.mkdir(parents=True, exist_ok=True)
MANIPULATED_DIR.mkdir(parents=True, exist_ok=True)

# Quantidades
POSTS_PER_PLATFORM = 20
MANIPULATIONS_PER_POST = 3

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

# Cores para avatares
AVATAR_COLORS = [
    '#1DA1F2', '#E1306C', '#25D366', '#FF6900', '#8B5CF6',
    '#EC4899', '#10B981', '#F59E0B', '#6366F1', '#EF4444',
    '#06B6D4', '#84CC16', '#F97316', '#A855F7', '#14B8A6'
]
