import random
import os
from DragModulo import DragImg

def inicializar(modo):
    img_list = []
    path = "ImagesPNG"
    files = os.listdir(path)

    if modo == 1:
        # MODO TESTE
        for x, nome in enumerate(files):
            imgType = 'png' if 'png' in nome else 'jpg'
            img_list.append(DragImg(f'{path}/{nome}', [100 + x * 200, 400], [100 + x * 200, 50], imgType, scale=0.5))

    elif modo == 2:
        # MODO JOGO
        escolhidos = random.sample(files, 2)
        for x, nome in enumerate(escolhidos):
            imgType = 'png' if 'png' in nome else 'jpg'

            # Criamos um objeto temporário para saber o tamanho da imagem (size)
            temp_obj = DragImg(f'{path}/{nome}', [0, 0], [0, 0], imgType, scale=0.5)
            h, w = temp_obj.size

            # --- VALIDAÇÃO DO ALVO (Target) ---
            tentativas = 0
            while tentativas < 50:  # Limite de tentativas para não travar o PC
                pos_alvo = [random.randint(100, 1000), random.randint(50, 250)]
                if not checar_overlap(pos_alvo, (w, h), img_list):
                    temp_obj.posTarget = pos_alvo
                    break
                tentativas += 1

            # --- VALIDAÇÃO DA POSIÇÃO INICIAL (Origin) ---
            tentativas = 0
            while tentativas < 50:
                pos_inicial = [random.randint(100, 1000), random.randint(400, 600)]
                # Aqui você pode checar contra as posições iniciais já definidas
                if not any(
                        not (pos_inicial[0] + w < obj.posOrigin[0] or pos_inicial[0] > obj.posOrigin[0] + obj.size[1] or \
                             pos_inicial[1] + h < obj.posOrigin[1] or pos_inicial[1] > obj.posOrigin[1] + obj.size[0])
                        for obj in img_list):
                    temp_obj.posOrigin = pos_inicial
                    break
                tentativas += 1

            img_list.append(temp_obj)

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