import random
import os
from objects.puzzle_piece import PuzzlePiece

def generate_basic_level(dificuldade=2):
    """Inicia a fase, carregando as imagens de acordo com a fase"""
    PuzzlePiece_list = []
    
    # Define a pasta base de assets de forma segura
    base_path = "assets"
    pasta_origem = os.path.join(base_path, "imagesPNG")
    pasta_alvo = os.path.join(base_path, "imagesTarget")
    
    # Garantir que as pastas existam
    if not os.path.exists(pasta_origem):
        print(f"Erro: Pasta {pasta_origem} não encontrada!")
        return []

    files = [f for f in os.listdir(pasta_origem) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    qtd_pecas = min(len(files), dificuldade)
    escolhidos = random.sample (files, qtd_pecas)

    for nome in escolhidos:
        caminho = os.path.join(pasta_origem, nome)
        caminhoTarget = os.path.join(pasta_alvo, nome)

        w, h = 200, 200

        # --- VALIDAÇÃO DO ALVO (Target) ---
        pos_target = encontrar_posicao_livre(PuzzlePiece_list, w, h, (100, 1000), (50, 250), "target")

        # --- VALIDAÇÃO DA POSIÇÃO INICIAL (Origin) ---
        pos_origin = encontrar_posicao_livre(PuzzlePiece_list, w, h, (100, 1000), (400, 600), "origin")

        # cria o objeto
        piece_object = PuzzlePiece(caminho, caminhoTarget, pos_origin, pos_target)
        PuzzlePiece_list.append(piece_object)
    return PuzzlePiece_list


def encontrar_posicao_livre(lista_existente, w, h, range_x, range_y, tipo):
    """Função auxiliar para evitar repetição de código de overlap"""
    tentativas = 0
    while tentativas < 50:
        pos = [random.randint(range_x[0], range_x[1]), random.randint(range_y[0], range_y[1])]
        
        overlap = False
        for outro in lista_existente:
            # Pega a posição correta dependendo se estamos checando Target ou Origin
            ox, oy = outro.posTarget if tipo == "target" else outro.posOrigin
            ow, oh = outro.size
            
            # Lógica de colisão de retângulos (AABB)
            if not (pos[0] + w < ox or pos[0] > ox + ow or
                    pos[1] + h < oy or pos[1] > oy + oh):
                overlap = True
                break
        
        if not overlap:
            return pos
        tentativas += 1
    
    # Fallback caso não ache lugar
    return [200 + len(lista_existente) * 220, 150 if tipo == "target" else 500]


def generate_fixed_level(qtd_pecas=2, w=160, h=160):
    """
    Gera um nível com pontos de origem e alvos fixos e definidos (não-aleatórios).
    Objetos são gerados no lado esquerdo da tela e devem ser levados até os alvos no lado direito,
    percorrendo a tela e desviando de possíveis barreiras centrais.
    """
    PuzzlePiece_list = []

    base_path = "assets"
    pasta_origem = os.path.join(base_path, "imagesPNG")
    pasta_alvo = os.path.join(base_path, "imagesTarget")

    if not os.path.exists(pasta_origem):
        print(f"Erro: Pasta {pasta_origem} não encontrada!")
        return []

    # Lista ordenada para manter a seleção previsível e consistente (não-aleatória)
    files = sorted([f for f in os.listdir(pasta_origem) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

    if not files:
        print("Erro: Nenhuma imagem encontrada para o nível!")
        return []

    # Posições pré-definidas: Origem à esquerda, Alvo à direita
    posicoes_definidas = [
        {"origem": [120, 130], "alvo": [980, 130]},
        {"origem": [120, 430], "alvo": [980, 430]},
        {"origem": [120, 280], "alvo": [980, 280]},
        {"origem": [120, 20],  "alvo": [980, 20]}
    ]

    total_pecas = min(qtd_pecas, len(files), len(posicoes_definidas))

    for i in range(total_pecas):
        nome = files[i]
        caminho = os.path.join(pasta_origem, nome)
        caminhoTarget = os.path.join(pasta_alvo, nome)

        pos_origin = list(posicoes_definidas[i]["origem"])
        pos_target = list(posicoes_definidas[i]["alvo"])

        piece_object = PuzzlePiece(caminho, caminhoTarget, pos_origin, pos_target, width=w, height=h)
        PuzzlePiece_list.append(piece_object)

    return PuzzlePiece_list