# CV Puzzle Game

## Visão Geral

O **CV Puzzle Game** é um jogo de quebra-cabeça baseado em webcam que combina detecção de mãos com renderização 2D. O jogador arrasta peças virtuais para encaixá-las em alvos, usando gestos de mão como cursor e clique.

O projeto utiliza **OpenCV** para captura de vídeo, **CVZone / MediaPipe** para detecção de mãos e **Pygame** para a interface e desenho do jogo.

---

## 1. Funcionamento

### 1.1 Fluxo do Jogo

1. O jogo inicia em `main.py` com a janela do Pygame e a captura de webcam.
2. A cada frame, a imagem da câmera é lida e espelhada.
3. `systems/hand_controller.py` processa o frame para detectar a mão e determinar o cursor e o estado de clique.
4. O frame da câmera é convertido para Pygame e usado como fundo do jogo.
5. A máquina de estados controla as telas:
   - `menu`
   - `fases`
   - `jogando`
   - `vitória`
6. Quando o jogador escolhe uma fase, o nível correspondente é carregado:
   - `levels/level_1.py` → 2 peças
   - `levels/level_2.py` → 4 peças
7. O jogo exibe as peças e seus alvos.
8. O jogador move a peça selecionada pelo cursor e, ao aproximar o dedo indicador do médio, ativa o clique.
9. Se a peça chega próxima ao alvo, ela se encaixa automaticamente e fica fixa.
10. Quando todas as peças estão encaixadas, a tela de vitória é exibida.

### 1.2 Entrada por movimento de mão

- O cursor é calculado a partir do landmark do dedo indicador.
- O clique é detectado pela distância entre o dedo indicador e o dedo médio.
- Distância menor que 60 pixels ativa o clique.
- O controle é feito por `cvzone.HandTrackingModule.HandDetector`.

### 1.3 Renderização

- A câmera é usada como plano de fundo.
- As imagens de alvo (`spriteTarget`) são desenhadas primeiro.
- As peças (`sprite`) são desenhadas acima dos alvos.
- A tela de vitória é exibida por cima do jogo quando o usuário completa o nível.

---

## 2. Tecnologias Utilizadas

### 2.1 Dependências principais

- `pygame` — renderização 2D, interface e eventos
- `opencv-python` — captura de vídeo da webcam e manipulação de frames
- `opencv-contrib-python` — usado pelo `cvzone` para detecção de mão
- `cvzone` — wrapper para `MediaPipe` com detecção de mão mais simples
- `mediapipe` — detecção de mãos e landmarks
- `numpy` — conversão entre arrays OpenCV e superfícies Pygame

### 2.2 Dependências do ambiente

O arquivo `requirements.txt` também inclui outras bibliotecas instaladas no ambiente, como:

- `Pillow`
- `SciPy`
- `Matplotlib`
- `JAX`
- `sounddevice`

> Observação: `pygame` não está pinado em `requirements.txt` atualmente, mas é exigido pelo código.

---

## 3. Arquitetura

### 3.1 Estrutura atual do projeto

```
CVPuzzleGame/
├── README.md
├── main.py
├── requirements.txt
├── assets/
│   ├── imagesPNG/
│   └── imagesTarget/
├── levels/
│   ├── level_1.py
│   └── level_2.py
├── objects/
│   └── puzzle_piece.py
├── systems/
│   ├── clickDetection.py
│   ├── game_manager.py
│   ├── hand_controller.py
│   ├── level_generator.py
│   └── render.py
├── ui/
│   ├── button.py
│   ├── level_select.py
│   ├── main_menu.py
│   └── victory_screen.py
└── venv/
```

### 3.2 Descrição dos principais módulos

#### `main.py`
- Ponto de entrada do jogo.
- Cria a janela Pygame e o loop principal.
- Gerencia estados do jogo e transições de tela.
- Coordena captura de webcam, processamento de mão e desenho.

#### `systems/hand_controller.py`
- Detecta mãos e calcula cursor e clique.
- Controla seleção e arraste das peças.
- Retorna o cursor, o estado de clique, a peça selecionada e a imagem processada.

#### `systems/level_generator.py`
- Gera a configuração básica do nível a partir de imagens em `assets/`.
- Seleciona imagens aleatórias para as peças e alvos.
- Evita sobreposição de posições usando colisão AABB.

#### `systems/game_manager.py`
- Verifica se todas as peças já foram encaixadas.
- Retorna verdadeiro quando o jogador vence.

#### `systems/render.py`
- Desenha os alvos e as peças na tela.
- Mantém o desenho simples e sequencial para respeitar as camadas.

#### `objects/puzzle_piece.py`
- Define a classe `PuzzlePiece`.
- Carrega e redimensiona sprites de peça e alvo.
- Gerencia posição, colisão e lógica de snap.

#### `ui/button.py`
- Classe reutilizável para botões com comportamento hover.
- Renderiza o botão e detecta quando o cursor está sobre ele.

#### `ui/main_menu.py`
- Tela principal com os botões de `FASES` e `SAIR`.
- Retorna o próximo estado do jogo.

#### `ui/level_select.py`
- Tela de seleção de fases com três botões.
- Atualmente oferece `FASE 1`, `FASE 2` e `FASE 3`.
- Somente `FASE 1` e `FASE 2` estão implementadas em `main.py`.

#### `ui/victory_screen.py`
- Exibe mensagem de vitória com transparência.
- Oferece botão `CONTINUAR` para retornar ao menu de fases.

#### `levels/level_1.py` e `levels/level_2.py`
- Classes pequenas que carregam níveis predefinidos.
- Chamam `generate_basic_level()` com diferentes quantidades de peças.

#### `systems/clickDetection.py`
- Módulo alternativo para processar entrada de mão.
- Hoje não é usado diretamente pelo loop principal, mas mantém lógica de detecção como referência.

---

## 4. Fluxo de execução

1. `main.py` inicia o jogo e define o estado `menu`.
2. A câmera é aberta via OpenCV.
3. O loop principal processa eventos Pygame e frames da câmera.
4. `systems/hand_controller.py` detecta o cursor e o clique.
5. A imagem da câmera é convertida e desenhada como fundo.
6. A interface renderiza o menu, seleção de fase, jogo ou vitória.
7. O estado muda conforme as ações do jogador.
8. Se houver vitória, o jogo exibe a tela de vitória e espera a ação do usuário.

---

## 5. Observações sobre a organização atual

- O código está organizado em pacotes para separar UI, lógica de jogo, objetos e sistemas.
- Há módulos de suporte (`systems/clickDetection.py`) que não estão conectados ao fluxo principal.
- A seleção de fase no `ui/level_select.py` sugere três fases, mas apenas duas fases são carregadas em `main.py`.
- O diretório `assets/` armazena as imagens das peças e alvos.
- O diretório `venv/` contém o ambiente virtual e não faz parte do código-fonte principal.
