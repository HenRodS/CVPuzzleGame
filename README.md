# CV Puzzle Game - Documentação

## 1. Funcionamento

### 1.1 Visão Geral do Jogo

O **CV Puzzle Game** é um jogo de quebra-cabeça interativo que utiliza **visão computacional** para detectar movimentos de mão e permitir que o jogador arraste peças de puzzle usando gestos. O jogo combina **OpenCV**, **Pygame** e **MediaPipe** para criar uma experiência imersiva onde o jogador interage com o jogo por meio de webcam.

### 1.2 Fluxo de Gameplay

#### **Menu Principal**
- O jogador inicia na tela de menu com duas opções: "FASES" e "SAIR"
- O cursor do mouse é controlado pela posição da mão detectada pela câmera
- Clique é simulado pelo gesto de aproximar o polegar e o dedo indicador (distância < 60 pixels)

#### **Seleção de Fase**
- O jogador escolhe uma fase (Fase 1: 2 peças, Fase 2: 4 peças)
- Cada fase carrega um número diferente de imagens de puzzle
- As peças são selecionadas aleatoriamente da pasta de assets

#### **Jogo Ativo (Jogando)**
1. **Renderização Inicial**:
   - Peças de puzzle aparecem em posições aleatórias no lado esquerdo/centro da tela
   - Alvos (targets) aparecem em posições fixas no lado direito da tela
   - Cada peça tem uma cor aleatória e um alvo correspondente

2. **Interação com Peças**:
   - O jogador detecta peças com a mão
   - Ao fazer o gesto de clique (polegar e indicador próximos), a peça é selecionada
   - A peça segue o cursor (posição da mão) enquanto o clique está ativo
   - Quando o jogador solta (aumenta a distância entre polegar e indicador), a peça é liberada

3. **Sistema de Encaixe (Snap)**:
   - Quando uma peça se aproxima do alvo (distância < 50 pixels em X e Y)
   - A peça "encaixa" automaticamente no alvo
   - A borda da peça muda de uma cor aleatória para verde, indicando sucesso
   - A peça encaixada não pode mais ser movida

4. **Vitória**:
   - Quando todas as peças são encaixadas nos seus alvos, a tela de vitória é exibida
   - Exibe a mensagem: "PARABÉNS, VOCÊ VENCEU!"
   - O jogador clica no botão "CONTINUAR" para retornar ao menu de fases

### 1.3 Detecção de Mão e Cursor

- **HandDetector (MediaPipe)**: Detecta landmarks (pontos-chave) da mão
- **Cursor**: Posição do dedo indicador (landmark 8)
- **Clique**: Calculado pela distância entre o dedo indicador (landmark 8) e dedo médio (landmark 12)
  - Se distância < 60 pixels: clique ativo
  - Se distância >= 60 pixels: clique inativo

### 1.4 Renderização Visual

- **Camada 1**: Alvos (targets) são desenhados ao fundo
- **Camada 2**: Peças (imagens arrastáveis) são desenhadas à frente
- Bordes em torno de cada elemento indicam seu estado:
  - Verde (para peças encaixadas)
  - Cor aleatória (para peças soltas)
  - Branca (para alvos)

---

## 2. Tecnologias Utilizadas

### 2.1 Bibliotecas Principais

| Tecnologia | Versão | Propósito |
|---|---|---|
| **OpenCV** | 4.13.0.92 | Captura e processamento de frames de vídeo da webcam |
| **Pygame** | (não especificado) | Renderização gráfica, interface do jogo e eventos |
| **MediaPipe** | 0.10.13 | Detecção de mãos e landmarks (pontos-chave) |
| **CVZone** | 1.6.1 | Wrapper simplificado para MediaPipe |
| **NumPy** | 2.4.2 | Operações com arrays e processamento de imagens |

### 2.2 Dependências Adicionais

| Biblioteca | Versão | Propósito |
|---|---|---|
| **Pillow** | 12.1.1 | Processamento e manipulação de imagens |
| **SciPy** | 1.17.1 | Computações científicas e cálculos matemáticos |
| **Matplotlib** | 3.10.8 | Visualização de dados (se necessário) |
| **JAX** | 0.9.1 | Computação numérica acelerada |
| **SoundDevice** | 0.5.5 | Processamento de áudio (para sons futuros) |

### 2.3 Stack Tecnológico

```
┌─────────────────────────────────────────┐
│         APLICAÇÃO PRINCIPAL             │
│         (main.py - Pygame Loop)         │
└─────────────────────────────────────────┘
           ↓                    ↓
    ┌────────────────┐   ┌──────────────┐
    │  OpenCV Cap    │   │   Interface  │
    │ (webcam feed)  │   │  (Botões UI) │
    └────────────────┘   └──────────────┘
           ↓
    ┌────────────────┐
    │  CVZone Handler│
    │ (Hand Detection│
    │   + Landmarks) │
    └────────────────┘
           ↓
    ┌────────────────────────┐
    │  Lógica de Jogo        │
    │ (DragModulo, Render)   │
    └────────────────────────┘
```

---

## 3. Arquitetura

### 3.1 Estrutura de Diretórios

```
CVPuzzleGame/
├── main.py                    # Ponto de entrada, loop principal do Pygame
├── ManagerJogo.py             # Gerenciador de fases, inicialização de objetos
├── Interface.py               # Telas da UI (menu, fases, vitória)
├── Render.py                  # Renderização visual do jogo
├── DragModulo.py              # Classe DragImg (peças de puzzle)
├── clickDetection.py          # Processamento de entrada de mão
├── levels.py                  # Configuração de níveis (não utilizado atualmente)
├── requirements.txt           # Dependências do projeto
├── assets/
│   ├── imagesPNG/             # Imagens de peças do puzzle
│   └── imagesTarget/          # Imagens alvo (targets) para encaixe
└── venv/                      # Ambiente virtual Python
```

### 3.2 Diagrama de Classes

#### **Classe: Botao** (Interface.py)
```python
class Botao:
    - texto: str
    - rect: pygame.Rect
    - cor_base: tuple RGB
    - cor_hover: tuple RGB
    - fonte: pygame.font
    
    + desenhar(tela, cursor) → bool
```

**Responsabilidade**: Renderizar botões interativos na interface com efeito hover.

#### **Classe: DragImg** (DragModulo.py)
```python
class DragImg:
    - path: str                    # Caminho da imagem
    - pathTarget: str              # Caminho da imagem alvo
    - img: pygame.Surface          # Imagem carregada
    - imgTarget: pygame.Surface    # Imagem alvo carregada
    - rect: pygame.Rect            # Retângulo para colisão e posição
    - posOrigin: list [x, y]       # Posição inicial da peça
    - posTarget: list [x, y]       # Posição alvo para encaixe
    - isMatched: bool              # Estado de encaixe
    - size: tuple (w, h)           # Dimensões da peça
    - color: tuple RGB             # Cor aleatória da borda
    
    + __init__(path, pathTarget, posOrigin, posTarget, width=200, height=200)
    + update(cursor)               # Atualiza posição e verifica encaixe
```

**Responsabilidade**: Gerenciar uma peça de puzzle individual, incluindo sua posição, renderização e detecção de encaixe.

### 3.3 Fluxo de Dados

```
┌─────────────────────────────────────────────────────────────────┐
│                    LOOP PRINCIPAL (main.py)                     │
└─────────────────────────────────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │  1. Captura frame da webcam (OpenCV)  │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │  2. Detect mãos e landmarks (CVZone)  │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │  3. Calcula cursor e clique           │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │  4. Máquina de Estados                │
        │     - Menu                            │
        │     - Seleção de Fases                │
        │     - Jogando                         │
        │     - Vitória                         │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │  5. Renderiza tela (Pygame)           │
        │     - Fundo (frame da camera)         │
        │     - Elementos UI                    │
        │     - Peças e Alvos                   │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │  6. Atualiza display (60 FPS)         │
        └───────────────────────────────────────┘
```

### 3.4 Descrição de Módulos

#### **main.py** - Ponto de Entrada
- Inicializa Pygame e OpenCV
- Captura frames da webcam
- Detecta mãos com CVZone (HandDetector)
- Implementa a máquina de estados principal
- Coordena renderização e lógica do jogo
- Loop principal roda a 60 FPS

#### **ManagerJogo.py** - Gerenciador de Fases
- **Função `inicializar(dificuldade=2)`**:
  - Carrega imagens de `assets/imagesPNG/`
  - Seleciona aleatoriamente N imagens (baseado na dificuldade)
  - Cria objetos `DragImg` com posições aleatórias
  - Retorna lista de objetos do jogo

- **Função `encontrar_posicao_livre()`**:
  - Gera posições aleatórias sem sobreposição
  - Usa colisão AABB (Axis-Aligned Bounding Box)
  - Tenta até 50 vezes encontrar posição válida
  - Fallback: posiciona em locais pré-definidos

#### **Interface.py** - UI e Telas
- **Classe `Botao`**: Define botões interativos com hover effect
- **`tela_menu_pygame()`**: Renderiza menu principal
- **`tela_fases_pygame()`**: Renderiza seleção de fases
- **`tela_vitoria_pygame()`**: Renderiza tela de vitória com sobreposição

#### **Render.py** - Renderização Visual
- **Função `renderizar_jogo()`**:
  - Desenha alvos (targets) em camada inferior
  - Desenha peças (imagens) em camada superior
  - Conta peças encaixadas
  - Retorna contador de encaixes

#### **DragModulo.py** - Lógica de Peças
- **Classe `DragImg`**: Gerencia peças individuais
  - Carrega e redimensiona imagens
  - Detecta cliques/colisão de cursor
  - Atualiza posição enquanto selecionada
  - Implementa snap/encaixe automático

#### **clickDetection.py** - Processamento de Entrada (Não Utilizado Atualmente)
- **Função `processar_hand_input()`**: 
  - Encapsula lógica de detecção de mão
  - Pode ser integrada para modularizar código
  - Retorna imagem, cursor, clique e objeto selecionado

#### **levels.py** - Configuração de Níveis (Não Utilizado Atualmente)
- Dicionário com configurações de fases
- Pode ser expandido para suportar múltiplos níveis com diferentes propriedades

### 3.5 Padrões e Conceitos

#### **Máquina de Estados**
```python
Estado: "menu"
    ↓ [Clica em FASES]
Estado: "fases"
    ↓ [Seleciona fase]
Estado: "jogando"
    ↓ [Todas peças encaixadas]
Estado: "vitória"
    ↓ [Clica em CONTINUAR]
Estado: "fases"
```

#### **Sistema de Camadas de Renderização**
1. **Camada 0**: Frame da webcam (fundo)
2. **Camada 1**: Alvos (targets)
3. **Camada 2**: Peças (imagens arrastáveis)
4. **Camada 3**: UI (botões, texto)

#### **Colisão e Snap**
- **Detecção de seleção**: Retângulo colidepoint (AABB)
- **Snap (Encaixe)**: Quando distância euclidiana < 50 pixels
- **Previne re-movimento**: Flag `isMatched` desativa update

### 3.6 Fluxo de Interação Usuário

```
Usuario com mão na frente da câmera
        ↓
    HandDetector detecta landmarks
        ↓
    Calcula cursor = posição dedo indicador (landmark 8)
        ↓
    Calcula distância entre indicador e médio (landmark 8 e 12)
        ↓
    Se distância < 60:
        ├─→ clicou = True
        ├─→ Se cursor colide com peça não-encaixada
        │   └─→ selectedImg = peça
        └─→ Atualiza posição de selectedImg para cursor
    Senão:
        └─→ clicou = False
        └─→ selectedImg = None
        ↓
    DragImg.update() verifica snap
        ├─→ Se distância < 50 pixels do alvo
        │   ├─→ Encaixa peça (isMatched = True)
        │   └─→ Muda cor da borda para verde
        └─→ Retorna posição atualizada
        ↓
    Renderiza_jogo() desenha peça em nova posição
```

### 3.7 Dependências Entre Módulos

```
main.py
├── Importa: pygame, numpy, cv2, cvzone, Interface, ManagerJogo, Render
├── Usa: HandDetector (cvzone), VideoCapture (cv2)
│
├─→ Interface.py
│   └── Importa: pygame, cv2, cvzone
│       Expõe: Botao, tela_menu_pygame, tela_fases_pygame, tela_vitoria_pygame
│
├─→ ManagerJogo.py
│   ├── Importa: pygame, random, os, DragModulo
│   ├── Usa: DragImg
│   └── Expõe: inicializar(), encontrar_posicao_livre()
│
├─→ Render.py
│   ├── Importa: pygame
│   └── Expõe: renderizar_jogo()
│
└─→ DragModulo.py
    ├── Importa: pygame, random
    └── Expõe: DragImg (classe)
```

### 3.8 Fluxo de Assets

```
Carregar Assets:
├── imagesPNG/
│   ├── imagem1.png → carregada como img
│   ├── imagem2.png → carregada como img
│   └── ...
│
└── imagesTarget/
    ├── imagem1.png → carregada como imgTarget
    ├── imagem2.png → carregada como imgTarget
    └── ...

Processamento:
├── Redimensionamento: 200x200 (peça) e 210x210 (alvo)
├── Conversão: pygame.image.load() → pygame.Surface
└── Armazenamento: DragImg.img e DragImg.imgTarget
```

---

## Resumo da Arquitetura

O projeto segue uma **arquitetura modular com separação de responsabilidades**:

- **Captura e Processamento**: OpenCV + CVZone (entrada)
- **Renderização**: Pygame (saída visual)
- **Lógica de Jogo**: ManagerJogo + DragModulo + Render (processamento)
- **Interface**: Interface.py (UI e navegação)
- **Loop Principal**: main.py (orquestração)

Essa estrutura permite fácil expansão, manutenção e adição de novas funcionalidades sem impactar o resto da aplicação.
