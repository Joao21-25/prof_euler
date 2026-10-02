# Prof. Euler — Monitor Inteligente de Matemática

O **Prof. Euler** é um monitor de matemática desenvolvido com inteligência artificial, com o objetivo de apoiar estudantes no processo de aprendizagem por meio de orientações guiadas, exercícios e conteúdos de revisão.

Diferentemente de uma ferramenta que simplesmente fornece respostas, o projeto busca estimular o raciocínio do estudante, conduzindo-o por etapas para que desenvolva autonomia na resolução de problemas.

## Funcionalidades

* **Monitor com IA:** interação em linguagem natural para esclarecer dúvidas e orientar o raciocínio matemático.
* **Aprendizagem ativa:** instruções para que o tutor conduza o aluno por perguntas e explicações, em vez de entregar imediatamente a solução.
* **Exercícios:** questões de diferentes temas e níveis de dificuldade, incluindo geração e correção com IA.
* **Conteúdos de revisão:** materiais de apoio sobre frações, potências, produtos notáveis, raízes, funções, logaritmos e trigonometria.
* **Personalização:** seleção do nível de linguagem das explicações.
* **Gamificação:** sistema de XP, níveis e conquistas para acompanhar o progresso durante o uso.

## Tecnologias utilizadas

* **Python** — linguagem principal do projeto.
* **Streamlit** — desenvolvimento da interface web.
* **Google Gemini API** — integração com o modelo de inteligência artificial.

## Acesse o projeto

* **Aplicação online:** https://prof-euler.streamlit.app
* **Repositório:** https://github.com/Joao21-25/prof_euler

## Como executar localmente

1. Clone este repositório:

   ```bash
   git clone https://github.com/Joao21-25/prof_euler.git
   cd prof_euler
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv env
   ```

   No Windows:

   ```bash
   env\Scripts\activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure a variável de ambiente `GEMINI_API_KEY` com uma chave válida da Google Gemini API. Não compartilhe essa chave nem a envie ao GitHub.

5. Execute a aplicação:

   ```bash
   streamlit run app.py
   ```

## Sobre o projeto

O Prof. Euler é um protótipo funcional em desenvolvimento. A proposta é explorar o uso da inteligência artificial como ferramenta de apoio educacional, com foco em aprendizagem ativa, personalização e maior autonomia dos estudantes.
