import pygame
import random
import os
from DragModulo import DragImg

def inicializar(dificuldade=2):
    """Inicia a fase, carregando as imagens de acordo com a fase"""
    img_list = []
    
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
        pos_target = encontrar_posicao_livre(img_list, w, h, (100, 1000), (50, 250), "target")

        # --- VALIDAÇÃO DA POSIÇÃO INICIAL (Origin) ---
        pos_origin = encontrar_posicao_livre(img_list, w, h, (100, 1000), (400, 600), "origin")

        # cria o objeto
        img_obj = DragImg(caminho, caminhoTarget, pos_origin, pos_target)
        img_list.append(img_obj)

    return img_list


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