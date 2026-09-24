import streamlit as st
import os
import google.generativeai as genai

# Configuração Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-flash-latest")

PROMPT = """
Você é o Prof. Euler, monitor de matemática para universitários iniciantes.

Seu papel é ensinar por aprendizagem ativa, nunca resolver diretamente.

MISSÃO
Conduzir o aluno ao raciocínio correto por perguntas guiadas.

REGRAS

1. Nunca entregue a resposta final imediatamente.

2. Sempre identifique brevemente:
- tipo de problema
- objetivo matemático

3. Explique de forma clara e acessível.

4. Adapte o nível:
- aluno com dificuldade → explicação mais detalhada
- aluno demonstrando domínio → seja mais direto

5. Após cada explicação, faça apenas UMA pergunta guiada.

6. Sempre espere participação antes de avançar.

7. Ao avaliar respostas:
- diga se está correta, parcial ou incorreta
- explique brevemente
- conduza o próximo passo

8. Ao detectar erro:
- mostre exatamente onde ocorreu
- explique o motivo
- ajude a corrigir sem resolver tudo

9. Se o aluno pedir resposta direta:
recuse educadamente e continue guiando.

10. Se houver muita dificuldade:
resolva exemplo semelhante.

ESTILO

Seja:
- didático
- objetivo
- paciente
- natural

Evite:
- textos longos
- repetições
- excesso de explicação

FORMATO

Cada resposta deve ter:

1. Validação breve
2. Explicação curta
3. Uma pergunta guiada final
"""

EXERCICIOS = {

    "Frações": [

        {
            "nivel": "Fácil",
            "pergunta": "Calcule: 1/2 + 1/3",
            "resposta": "5/6"
        },

        {
            "nivel": "Médio",
            "pergunta": "Calcule: 3/4 + 5/6",
            "resposta": "19/12"
        },

        {
            "nivel": "Difícil",
            "pergunta": "Calcule: 5/8 - 1/3 + 7/12",
            "resposta": "7/8"
        }

    ],

    "Potências": [

        {
            "nivel": "Fácil",
            "pergunta": "Calcule: 2³ · 2²",
            "resposta": "32"
        },

        {
            "nivel": "Médio",
            "pergunta": "Simplifique: (3²)⁴",
            "resposta": "3⁸"
        },

        {
            "nivel": "Difícil",
            "pergunta": "Simplifique: 2⁵ · 2⁻²",
            "resposta": "8"
        }

    ],

    "Produtos notáveis": [

        {
            "nivel": "Fácil",
            "pergunta": "Desenvolva: (x + 3)²",
            "resposta": "x² + 6x + 9"
        },

        {
            "nivel": "Médio",
            "pergunta": "Desenvolva: (2x - 5)²",
            "resposta": "4x² - 20x + 25"
        },

        {
            "nivel": "Difícil",
            "pergunta": "Simplifique: (x + 7)(x - 7)",
            "resposta": "x² - 49"
        }

    ],

    "Raízes": [

        {
            "nivel": "Fácil",
            "pergunta": "Calcule: √25",
            "resposta": "5"
        },

        {
            "nivel": "Médio",
            "pergunta": "Simplifique: √72",
            "resposta": "6√2"
        },

        {
            "nivel": "Difícil",
            "pergunta": "Simplifique: √180",
            "resposta": "6√5"
        }

    ],

    "Funções": [

        {
            "nivel": "Fácil",
            "pergunta": "Dada f(x) = 2x + 3, calcule f(4).",
            "resposta": "11"
        },

        {
            "nivel": "Médio",
            "pergunta": "Determine a raiz da função f(x) = 3x - 12.",
            "resposta": "4"
        },

        {
            "nivel": "Difícil",
            "pergunta": "Determine o domínio de f(x) = 1/(x - 5).",
            "resposta": "x ≠ 5"
        }

    ],

    "Logaritmos": [

        {
            "nivel": "Fácil",
            "pergunta": "Calcule: log₂(8).",
            "resposta": "3"
        },

        {
            "nivel": "Médio",
            "pergunta": "Calcule: log₃(81).",
            "resposta": "4"
        },

        {
            "nivel": "Difícil",
            "pergunta": "Resolva: log₂(x) = 5.",
            "resposta": "32"
        }

    ],

    "Trigonometria": [

        {
            "nivel": "Fácil",
            "pergunta": "Em um triângulo retângulo, o cateto oposto mede 3 e a hipotenusa mede 5. Qual é o seno do ângulo?",
            "resposta": "3/5"
        },

        {
            "nivel": "Médio",
            "pergunta": "Em um triângulo retângulo, o cateto adjacente mede 4 e a hipotenusa mede 5. Qual é o cosseno do ângulo?",
            "resposta": "4/5"
        },

        {
            "nivel": "Difícil",
            "pergunta": "Se tg(x) = 3/4, determine o seno de x.",
            "resposta": "3/5"
        }

    ]
}

st.set_page_config(
    page_title="Monitor de Matemática",
    page_icon="📘",
    layout="wide"
)

# Histórico
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [PROMPT]
            }
        ]
    )

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "questoes" not in st.session_state:
    st.session_state.questoes = 0

if "streak" not in st.session_state:
    st.session_state.streak = 1

if "conquistas" not in st.session_state:
    st.session_state.conquistas = []

if "nivel" not in st.session_state:
    st.session_state.nivel = "Iniciante"

def atualizar_nivel():
    xp = st.session_state.xp

    if xp >= 2000:
        st.session_state.nivel = "Mestre do Cálculo"

    elif xp >= 1000:
        st.session_state.nivel = "Mestre Algébrico"

    elif xp >= 600:
        st.session_state.nivel = "Explorador"

    elif xp >= 300:
        st.session_state.nivel = "Estudante"

    elif xp >= 100:
        st.session_state.nivel = "Aprendiz"

    else:
        st.session_state.nivel = "Iniciante"


def ganhar_xp(valor):
    st.session_state.xp += valor
    atualizar_nivel()

def verificar_conquistas():

    if (
        st.session_state.questoes >= 10
        and "Primeiros Passos" not in st.session_state.conquistas
    ):
        st.session_state.conquistas.append("Primeiros Passos")

    if (
        st.session_state.xp >= 100
        and "Aprendiz Matemático" not in st.session_state.conquistas
    ):
        st.session_state.conquistas.append("Aprendiz Matemático")

    if (
        st.session_state.xp >= 500
        and "Persistente" not in st.session_state.conquistas
    ):
        st.session_state.conquistas.append("Persistente")

if "questoes" not in st.session_state:
    st.session_state.questoes = 0

st.sidebar.write(
    f"**Questões resolvidas:** {st.session_state.questoes}"
)

st.sidebar.metric(
    "Questões resolvidas",
    st.session_state.questoes
)

st.sidebar.metric(
    "Sequência",
    f"{st.session_state.streak} dias 🔥"
)

if st.session_state.xp < 100:
    objetivo = 100
elif st.session_state.xp < 300:
    objetivo = 300
elif st.session_state.xp < 600:
    objetivo = 600
elif st.session_state.xp < 1000:
    objetivo = 1000
else:
    objetivo = 2000

st.sidebar.progress(
    min(st.session_state.xp / objetivo, 1.0)
)

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

    # Sistema de exercícios
if "exercicio_gerado" not in st.session_state:
    st.session_state.exercicio_gerado = None

if "resposta_exercicio" not in st.session_state:
    st.session_state.resposta_exercicio = None

if "exercicio_corrigido" not in st.session_state:
    st.session_state.exercicio_corrigido = False

if "acertos" not in st.session_state:
    st.session_state.acertos = 0

if "erros" not in st.session_state:
    st.session_state.erros = 0

if "sequencia_acertos" not in st.session_state:
    st.session_state.sequencia_acertos = 0

if "interacoes_xp" not in st.session_state:
    st.session_state.interacoes_xp = 0

if "xp_exercicio" not in st.session_state:
    st.session_state.xp_exercicio = False

def gerar_exercicio_ia(tema, dificuldade):
    prompt_exercicio = f"""
    Você é um professor de matemática.

    Gere UM exercício de matemática sobre:

    Tema: {tema}
    Dificuldade: {dificuldade}

    O exercício deve ser adequado para estudantes universitários
    iniciantes.

    Regras:

    1. Gere apenas um exercício.
    2. Não resolva o exercício.
    3. Não forneça a resposta junto com o enunciado.
    4. O exercício deve ter uma resposta objetiva.
    5. Evite ambiguidades.
    6. Use matemática corretamente.

    Retorne apenas o enunciado do exercício.
    """

    resposta = model.generate_content(prompt_exercicio)

    return resposta.text

def corrigir_exercicio_ia(tema, exercicio, resposta_aluno):

    prompt_correcao = f"""
    Você é um professor de matemática.

    Tema:
    {tema}

    Exercício:
    {exercicio}

    Resposta do aluno:
    {resposta_aluno}

    Analise a resposta do aluno.

    Responda obrigatoriamente neste formato:

    RESULTADO: CORRETA ou INCORRETA

    EXPLICAÇÃO:
    Explique brevemente por que a resposta está correta ou incorreta.

    DICA:
    Se estiver incorreta, dê uma dica para o aluno tentar novamente.
    Não entregue a resposta final imediatamente.

    Seja didático e objetivo.
    """

    resposta = model.generate_content(prompt_correcao)

    return resposta.text

st.sidebar.title("📚 Central de Apoio")

st.sidebar.markdown("---")

st.sidebar.subheader("👤 Seu progresso")

st.sidebar.write(
    f"**Nível:** {st.session_state.nivel}"
)

st.sidebar.write(
    f"**XP:** {st.session_state.xp}"
)

proximo_nivel = 100

if st.session_state.xp < 100:
    proximo_nivel = 100
elif st.session_state.xp < 300:
    proximo_nivel = 300
elif st.session_state.xp < 600:
    proximo_nivel = 600
elif st.session_state.xp < 1000:
    proximo_nivel = 1000
else:
    proximo_nivel = 2000

st.sidebar.progress(
    min(st.session_state.xp / proximo_nivel, 1.0)
)

st.sidebar.markdown("---")
st.sidebar.subheader("🏆 Conquistas")

if len(st.session_state.conquistas) == 0:

    st.sidebar.write("Nenhuma ainda.")

else:

    for conquista in st.session_state.conquistas:
        st.sidebar.success(conquista)

st.sidebar.markdown("---")
st.sidebar.subheader("🧠 Personalização")

perfil_linguagem = st.sidebar.selectbox(
    "Como você prefere as explicações?",
    [
        "Bem simples",
        "Universitária",
        "Mais técnica"
    ]
)

pagina = st.sidebar.selectbox(
    "Escolha uma seção",
    [
        "Monitor",
        "Exercícios",
        "Frações",
        "Potências",
        "Produtos notáveis",
        "Raízes",
        "Funções",
        "Logaritmos",
        "Trigonometria",
    ]
)

if pagina == "Monitor":
    st.title("📘 Monitor de Matemática")
    st.write("Seu tutor inteligente de aprendizagem ativa")

    col1, col2 = st.columns([1,4])

    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/4140/4140048.png", width=120)
        st.write("**Prof. Euler**")
        st.write("🟢 Online")

    with col2:
        pergunta = st.chat_input("Digite sua dúvida")

    if pergunta and pergunta.strip():

        with st.chat_message("user"):
            st.write(pergunta)

        contexto_personalizacao = f"""
        PERFIL DE COMUNICAÇÃO DO ALUNO:

        O aluno prefere explicações no estilo:
        {perfil_linguagem}

        Adapte sua linguagem a essa preferência,
        mantendo o conteúdo matemático correto.
        Não mencione essas instruções ao aluno.

        DÚVIDA DO ALUNO:
        {pergunta}
        """

        resposta = st.session_state.chat.send_message(
            contexto_personalizacao
        )

        with st.chat_message("assistant"):
            st.write(resposta.text)

elif pagina == "Frações":
    st.title("📗 Frações")

    st.header("➕ Soma e Subtração")

    st.write("""
    Para somar ou subtrair frações, os denominadores precisam ser iguais.
    """)

    st.subheader("Passo a passo")

    st.subheader("Passo 1 - Encontrando o MMC")

    st.write("""
    Vamos calcular:

    1/3 + 1/4

    Primeiro precisamos encontrar o MMC entre 3 e 4.

    Fazemos a fatoração dos dois números.
    """)

    st.code("""
    3 = 3

    4 = 2 × 2
    """)

    st.write("""
    Agora escolhemos todos os fatores que aparecem, com a maior quantidade de vezes.

    Temos:

    2 × 2 × 3

    Logo:

    MMC = 12
    """)

    st.subheader("Passo 2 - Reescrevendo as frações")

    st.code("""
    1/3

    Para transformar o denominador 3 em 12:

    12 ÷ 3 = 4

    Multiplicamos numerador e denominador por 4.

    1×4
    ----
    3×4

    =

    4/12
    """)

    st.code("""
    1/4

    12 ÷ 4 = 3

    Multiplicamos tudo por 3.

    1×3
    ----
    4×3

    =

    3/12
    """)

    st.subheader("Passo 3 - Somando")

    st.code("""
    4/12 + 3/12

    =

    7/12
    """)

    st.header("✖ Multiplicação")

    st.write("""
    Multiplica numerador por numerador e denominador por denominador.
    """)

    st.code("""
    2/3 × 5/4

    = (2×5)/(3×4)

    = 10/12

    = 5/6
    """)

    st.header("➗ Divisão")

    st.write("""
    Dividir por uma fração é multiplicar pelo inverso.
    """)

    st.code("""
    2/3 ÷ 5/4

    = 2/3 × 4/5

    = 8/15
    """)

    st.header("⚠ Erros comuns")

    st.write("""
    ❌ Somar denominadores

    1/2 + 1/3 ≠ 2/5

    ✔ Correto:

    1/2 + 1/3 = 5/6
    """)

elif pagina == "Potências":
    st.title("📗 Potências")

    st.header("Produto de potências")

    st.code("""
    a² · a³

    = a^(2+3)

    = a⁵
    """)

    st.header("Divisão de potências")

    st.code("""
    a⁷ / a³

    = a^(7-3)

    = a⁴
    """)

    st.header("Potência de potência")

    st.code("""
    (a²)³

    = a^(2×3)

    = a⁶
    """)

    st.header("Expoente zero")

    st.code("""
    5⁰ = 1

    Qualquer número diferente de zero elevado a zero vale 1.
    """)

    st.header("Expoente negativo")

    st.code("""
    2⁻³

    = 1/2³

    = 1/8
    """)

    st.header("Raiz como potência")

    st.write("""
    Toda raiz pode ser escrita como uma potência.

    Isso é muito usado em álgebra e cálculo.
    """)

    st.code("""
    √a

    =

    a^(1/2)
    """)

    st.code("""
    ³√a

    =

    a^(1/3)
    """)

    st.code("""
    ⁴√a³

    =

    a^(3/4)
    """)
    


elif pagina == "Produtos notáveis":
    st.title("📗 Produtos Notáveis")

    st.header("Quadrado da soma")

    st.code("""
    (a+b)²

    = a² + 2ab + b²
    """)

    st.write("""
    Exemplo:

    (x+3)²

    = x² + 6x + 9
    """)

    st.header("Por que (a+b)² funciona?")

    st.write("""
    Imagine um quadrado cujo lado mede (a+b).

    Sua área total será:

    (a+b)²
    """)

    st.code("""
    +---------+----+
    |         |    |
    |   a²    |ab  |
    |         |    |
    +---------+----+
    |   ab    |b²  |
    +---------+----+
    """)

    st.write("""
    A área total é a soma das quatro regiões.

    Temos:

    a²

    +

    ab

    +

    ab

    +

    b²

    Como aparecem dois retângulos iguais:

    ab + ab = 2ab

    Logo:

    (a+b)² = a² + 2ab + b²
    """)

    st.header("Quadrado da diferença")

    st.code("""
    (a-b)²

    = a² - 2ab + b²
    """)

    st.write("""
    Exemplo:

    (x-4)²

    = x² - 8x + 16
    """)

    st.header("Soma pela diferença")

    st.code("""
    (a+b)(a-b)

    = a² - b²
    """)

    st.write("""
    Exemplo:

    (x+5)(x-5)

    = x² - 25
    """)

elif pagina == "Raízes":
    st.title("📗 Raízes")

    st.header("O que é raiz?")

    st.write("""
    A raiz procura um número que,
    multiplicado por ele mesmo,
    produz o valor dentro da raiz.
    """)

    st.code("""
    √25 = 5

    porque

    5 × 5 = 25
    """)

    st.header("Produto")

    st.code("""
    √(9×4)

    = √9 · √4

    = 3 · 2

    = 6
    """)

    st.header("Quociente")

    st.code("""
    √(16/4)

    = √16 / √4

    = 4/2

    = 2
    """)

    st.header("Simplificação")

    st.code("""
    √72

    = √(36×2)

    = √36 · √2

    = 6√2
    """)
    st.header("Potência como raiz")

    st.code("""
    16^(1/2)

    =

    √16

    =

    4
    """)

    st.code("""
    27^(1/3)

    =

    ³√27

    =

    3
    """)

elif pagina == "Funções":

    st.title("📗 Funções")

    st.header("O que é uma função?")

    st.write("""
    Uma função é uma regra que associa cada valor de entrada
    a exatamente um valor de saída.

    Exemplo:

    f(x) = 2x + 1

    Se x = 3:

    f(3) = 2·3 + 1 = 7
    """)

    st.header("Domínio")

    st.write("""
    O domínio é o conjunto dos valores que podem ser usados na entrada.

    Exemplo:

    f(x) = 1/(x-2)

    Não podemos dividir por zero.

    Portanto:

    x ≠ 2

    Domínio:

    D = ℝ - {2}
    """)

    st.header("Imagem")

    st.write("""
    A imagem é o conjunto dos valores que a função consegue produzir.

    Exemplo:

    f(x) = x²

    Não importa qual valor real seja usado,
    o resultado nunca será negativo.

    Imagem:

    Im = [0,+∞[
    """)

    st.header("Intuição")

    st.code("""
    Domínio           Imagem

    1  -------->  2

    2  -------->  5

    3  -------->  8
    """)

    st.write("""
    Cada elemento do domínio aponta para exatamente um elemento da imagem.

    Isso caracteriza uma função.
    """)

    st.header("Quando NÃO é função")

    st.code("""
    Domínio           Imagem

    1  -----> 2

    \\

    ------> 5
    """)

    st.write("""
    O número 1 possui duas imagens diferentes.

    Isso não pode acontecer em uma função.
    """)

    st.code("""
    1 ----> 5

    2 ----> 5

    3 ----> 5
    """)

    st.write("""
    Isso continua sendo função.

    Vários elementos podem chegar ao mesmo valor.

    O que não pode acontecer é um único elemento possuir duas imagens.
    """)

    st.header("Função Afim")

    st.code("""
    f(x)=ax+b

    Exemplo:

    f(x)=2x+3

    a = coeficiente angular

    b = coeficiente linear
    """)

    st.header("Função Quadrática")

    st.code("""
f(x)=ax²+bx+c

Exemplo:

f(x)=x²-4x+3

Gráfico em forma de parábola.
""")

    st.header("Erros comuns")

    st.write("""
    ❌ Confundir domínio com imagem

    Domínio:
    valores que entram

    Imagem:
    valores que saem
    """)

elif pagina == "Logaritmos":

    st.title("📗 Logaritmos")

    st.header("O que é logaritmo?")

    st.write("""
    Logaritmo responde à pergunta:

    'A que potência devo elevar a base
    para obter determinado número?'
    """)

    st.code("""
log₂(8)

Pergunta:

2 elevado a quanto dá 8?

2³ = 8

Logo:

log₂(8)=3
""")

    st.header("Condições de existência")

    st.write("""
    Para log_b(a):

    1) a > 0

    2) b > 0

    3) b ≠ 1
    """)

    st.header("Propriedade do Produto")

    st.code("""
log(a·b)

= log(a) + log(b)

Exemplo:

log(100)

= log(10·10)

= 1 + 1

= 2
""")

    st.header("Propriedade do Quociente")

    st.code("""
log(a/b)

= log(a) - log(b)
""")

    st.header("Propriedade da Potência")

    st.code("""
log(aⁿ)

= n·log(a)
""")

    st.header("Mudança de Base")

    st.code("""
log_b(a)

=

log(a)
/ log(b)
""")

    st.header("Exemplo de domínio")

    st.code("""
f(x)=log(2x-1)

2x-1 > 0

2x > 1

x > 1/2

Domínio:

]1/2,+∞[
""")

    st.header("Erros comuns")

    st.write("""
    ❌ log(a+b)

    NÃO é igual a

    log(a)+log(b)

    Essa propriedade não existe.
    """)

elif pagina == "Trigonometria":

    st.title("📗 Trigonometria Básica")

    st.header("Triângulo Retângulo")

    st.write("""
    É o triângulo que possui um ângulo de 90°.

    Seus lados recebem nomes especiais:

    Hipotenusa:
    lado oposto ao ângulo reto.

    Catetos:
    os outros dois lados.
    """)

    st.header("Teorema de Pitágoras")

    st.code("""
hipotenusa²

=

cateto1² + cateto2²

Exemplo:

x² = 3² + 4²

x² = 25

x = 5
""")

    st.header("Seno")

    st.write("""
    Relação entre:

    cateto oposto
    e
    hipotenusa
    """)

    st.code("""
sen(x)

=

cateto oposto
--------------
hipotenusa
""")

    st.header("Cosseno")

    st.write("""
    Relação entre:

    cateto adjacente
    e
    hipotenusa
    """)

    st.code("""
cos(x)

=

cateto adjacente
----------------
hipotenusa
""")

    st.header("Tangente")

    st.write("""
    Relação entre:

    cateto oposto
    e
    cateto adjacente
    """)

    st.code("""
tg(x)

=

cateto oposto
--------------
cateto adjacente
""")

    st.header("Macete SOH-CAH-TOA")

    st.write("""
    SOH

    Seno = Oposto / Hipotenusa

    CAH

    Cosseno = Adjacente / Hipotenusa

    TOA

    Tangente = Oposto / Adjacente
    """)

    st.header("Ângulos Notáveis")

    st.table({
        "Ângulo": ["30°","45°","60°"],
        "sen": ["1/2","√2/2","√3/2"],
        "cos": ["√3/2","√2/2","1/2"],
        "tg": ["√3/3","1","√3"]
    })

    st.header("Erros comuns")

    st.write("""
    ❌ Trocar cateto oposto pelo adjacente

    Sempre identifique primeiro
    qual é o ângulo de referência.
    """)

elif pagina == "Exercícios":

    st.title("🧠 Exercícios Personalizados")

    st.write("""
    Pratique matemática com exercícios selecionados
    ou gerados especialmente para você.
    """)

    st.markdown("---")

    modo = st.radio(
        "Escolha o modo de exercício:",
        [
            "Exercício gerado pela IA",
            "Exercício fixo"
        ]
    )

    if modo == "Exercício gerado pela IA":

        st.subheader("🤖 Gerar exercício com IA")

        tema = st.selectbox(
            "Escolha o tema:",
            [
                "Frações",
                "Potências",
                "Produtos notáveis",
                "Raízes",
                "Funções",
                "Logaritmos",
                "Trigonometria"
            ]
        )

        dificuldade = st.selectbox(
            "Escolha a dificuldade:",
            [
                "Fácil",
                "Médio",
                "Difícil"
            ]
        )

        if st.button("🎲 Gerar exercício"):

            with st.spinner("O Prof. Euler está preparando um exercício..."):

                exercicio = gerar_exercicio_ia(
                    tema,
                    dificuldade
                )

            st.session_state.exercicio_gerado = exercicio
            st.session_state.resposta_exercicio = None
            st.session_state.exercicio_corrigido = False

    if st.session_state.exercicio_gerado:

            st.markdown("---")

            st.subheader("📝 Seu exercício")

            st.info(
                st.session_state.exercicio_gerado
            )

            resposta_aluno = st.text_input(
                "Digite sua resposta:"
            )

            if st.button("🔍 Corrigir resposta"):

                if resposta_aluno:

                    with st.spinner("Analisando sua resposta..."):

                        correcao = corrigir_exercicio_ia(
                            tema,
                            st.session_state.exercicio_gerado,
                            resposta_aluno
                        )

                    st.session_state.resposta_exercicio = correcao

                    st.session_state.questoes += 1

                    if "RESULTADO: CORRETA" in correcao.upper():

                        st.session_state.acertos += 1
                        st.session_state.xp += 30

                    else:

                        st.session_state.erros += 1
                        st.session_state.xp += 5

                    atualizar_nivel()
                    verificar_conquistas()

            if st.session_state.resposta_exercicio:

                st.markdown("---")

                st.subheader("👨‍🏫 Feedback do Prof. Euler")

                st.write(
                    st.session_state.resposta_exercicio
                )
    elif modo == "Exercício fixo":

        st.subheader("📚 Exercício")

        exercicio = st.selectbox(
            "Escolha o conteúdo:",
            [
                "Frações",
                "Potências",
                "Produtos Notáveis",
                "Raízes",
                "Funções",
                "Logaritmos",
                "Trigonometria"
            ]
        )

        if exercicio == "Frações":

            enunciado = (
                "Calcule: 1/3 + 1/6"
            )

            resposta_correta = "1/2"

        elif exercicio == "Potências":

            enunciado = (
                "Simplifique: 2³ · 2²"
            )

            resposta_correta = "32"

        elif exercicio == "Produtos Notáveis":

            enunciado = (
                "Desenvolva: (x + 3)²"
            )

            resposta_correta = "x² + 6x + 9"

        elif exercicio == "Raízes":

            enunciado = (
                "Simplifique: √72"
            )

            resposta_correta = "6√2"

        elif exercicio == "Funções":

            enunciado = (
                "Determine f(3), sabendo que "
                "f(x) = 2x + 1."
            )

            resposta_correta = "7"

        elif exercicio == "Logaritmos":

            enunciado = (
                "Calcule: log₂(8)"
            )

            resposta_correta = "3"

        else:

            enunciado = (
                "Em um triângulo retângulo, "
                "o cateto oposto mede 3 e a hipotenusa mede 5. "
                "Qual é o seno do ângulo?"
            )

            resposta_correta = "3/5"

        st.info(enunciado)

        resposta_aluno = st.text_input(
            "Digite sua resposta:"
        )

        if st.button(
            "Verificar resposta",
            key="verificar_fixo"
        ):

            if not resposta_aluno.strip():

                st.warning(
                    "Digite uma resposta antes de verificar."
                )

            else:

                st.session_state.questoes += 1

                resposta_normalizada = (
                    resposta_aluno
                    .strip()
                    .lower()
                    .replace(" ", "")
                )

                correta_normalizada = (
                    resposta_correta
                    .strip()
                    .lower()
                    .replace(" ", "")
                )

                if resposta_normalizada == correta_normalizada:

                    st.success(
                        "🎉 Muito bem! Sua resposta está correta!"
                    )

                    st.session_state.acertos += 1

                    ganhar_xp(25)

                    st.write(
                        "🏆 **+25 XP**"
                    )

                else:

                    st.error(
                        "❌ Ainda não. Tente revisar o conteúdo "
                        "e pensar novamente."
                    )

                    ganhar_xp(5)

                    st.write(
                        "📘 **+5 XP por tentativa**"
                    )