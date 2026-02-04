import random
import os
from DragModulo import DragImg
from levels import levels

def inicializar(modo, fase=1):
    img_list = []
    level_config = levels[fase]

    path = level_config["pathObject"]
    pathTarget = level_config["pathTarget"]
    files = os.listdir(path)

    if modo == 2:
        # MODO JOGO (MODO TESTE NÃO IMPLEMENTADO)
        escolhidos = random.sample(files, level_config["objetos"])
        for nome in escolhidos:
            imgType = 'png' if 'png' in nome else 'jpg'
            caminho = f'{path}/{nome}'
            caminhoTarget = f'{pathTarget}/{nome}'

            # Criamos um objeto temporário para saber o tamanho da imagem (size)
            img_obj = DragImg(caminho, caminhoTarget, [0, 0], [0, 0], imgType)
            h, w = img_obj.size

            # --- VALIDAÇÃO DO ALVO (Target) ---
            tentativas = 0
            while tentativas < 50:  # Limite de tentativas para não travar o PC
                pos_alvo = [random.randint(100, 1000), random.randint(50, 250)]
                if not checar_overlap(pos_alvo, (w, h), img_list):
                    img_obj.posTarget = pos_alvo
                    break
                tentativas += 1
            else:
                # Se não encontrou posição → usa uma fixa ou ignora
                img_obj.posTarget = [300 + len(img_list) * 220, 150]

            # --- VALIDAÇÃO DA POSIÇÃO INICIAL (Origin) ---
            tentativas = 0
            while tentativas < 50:
                pos_inicial = [random.randint(100, 1000), random.randint(400, 600)]
                overlap = False
                for outro in img_list:
                    ox, oy = outro.posOrigin
                    ow, oh = outro.size
                    if not (pos_inicial[0] + w < ox or pos_inicial[0] > ox + ow or
                            pos_inicial[1] + h < oy or pos_inicial[1] > oy + oh):
                        overlap = True
                        break
                if not overlap:
                    img_obj.posOrigin = pos_inicial
                    break
                tentativas += 1
            else:
                # fallback
                img_obj.posOrigin = [200 + len(img_list) * 220, 500]

            img_list.append(img_obj)

    return img_list

def checar_overlap(new_pos, size, existing_list):
    nx, ny = new_pos
    nw, nh = size
    for imgObj in existing_list:
        ex, ey = imgObj.posTarget  # Ou posOrigin, dependendo do que quer validar
        ew, eh = imgObj.size

        # Lógica de intersecção de retângulos
        if not (nx + nw < ex or nx > ex + ew or ny + nh < ey or ny > ey + eh):
            return True  # Há sobreposição
    return False