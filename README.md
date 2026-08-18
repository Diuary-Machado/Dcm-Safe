<h1 align="center">🔐 DCM Safe</h1>
<p align="center"><b>Cofre Financeiro Pessoal Minimalista e Seguro</b></p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

---

## 🚀 Sobre o Projeto

O **DCM Safe** é uma aplicação web moderna e minimalista desenvolvida em **Python** e **Streamlit** para o gerenciamento e controle financeiro pessoal. O projeto foi estruturado com foco em boas práticas de engenharia de software, separação de responsabilidades, segurança de dados e uma interface de usuário refinada (Design System customizado).

---

## ⚙️ Funcionalidades

* **Autenticação Segura:** Sistema de login com cofre protegido por senha via `st.secrets`, garantindo isolamento e privacidade total dos registros.
* **Gestão Dinâmica de Lançamentos:** Controle ágil de entradas, saídas, filtragem por categorias e listagem detalhada.
* **Controle de Despesas Fixas:** Gerenciamento centralizado de compromissos recorrentes mensais.
* **Dashboard Analítico:** Métricas consolidadas, indicadores de saldo e visão geral do período.
* **Fechamento de Mês:** Ferramentas avançadas de auditoria, limpeza de dados e consolidação de ciclos financeiros.

---

## 📂 Arquitetura e Estrutura do Projeto

O projeto foi construído seguindo princípios de modularidade:

```text
DCM-SAFE/
├── .streamlit/         # Configurações e segredos da aplicação
│   └── secrets.toml    # Arquivo privado de senhas (ignorado pelo Git)
├── views/              # Módulos de telas e visualizações
│   ├── dashboard.py    # Painel de métricas e gráficos consolidados
│   ├── lancamentos.py  # Tela de registro de transações
│   ├── gerenciar.py    # Gerenciamento e edição de despesas fixas/avulsas
│   └── fechamento.py   # Auditoria e fechamento de ciclos mensais
├── app.py              # Ponto de entrada e roteador principal
├── auth.py             # Lógica de controle de acesso e autenticação
├── database.py         # Camada de persistência (conexões e queries SQL)
├── styles.py           # Design System (injeção de CSS customizado)
├── requirements.txt    # Dependências e bibliotecas do projeto
└── README.md           # Documentação oficial do projeto
```
🛠️ Como Executar Localmente
Siga os passos abaixo para clonar e rodar o projeto na sua máquina:

1. Clone o repositório
Bash
git clone [https://github.com/Diuary-Machado/Dcm-Safe.git](https://github.com/Diuary-Machado/Dcm-Safe.git)
cd Dcm-Safe
2. Crie e ative um ambiente virtual
No Windows (PowerShell):

Bash
python -m venv venv
venv\Scripts\activate
No Linux / macOS:

Bash
python3 -m venv venv
source venv/bin/activate
3. Instale as dependências
Bash
pip install -r requirements.txt
4. Configure a Senha de Acesso
Para que o sistema funcione, é necessário configurar a senha do cofre localmente:

Crie uma pasta chamada .streamlit na raiz do projeto (caso não exista).

Dentro dela, crie um arquivo chamado secrets.toml.

Adicione sua senha no seguinte formato:

Ini, TOML
APP_PASSWORD = "sua_senha_aqui"
(Nota: O arquivo secrets.toml é ignorado pelo Git e nunca será exposto publicamente).

5. Execute a aplicação
Bash
streamlit run app.py
💻 Tecnologias Utilizadas
Python: Lógica e Backend

Streamlit: Interface gráfica e reatividade

SQLite / Pandas: Persistência local e manipulação de dados

🔑 Como Alterar a Senha no Futuro
Sempre que você quiser mudar a senha do cofre, basta abrir o arquivo .streamlit/secrets.toml na sua máquina, alterar o valor de APP_PASSWORD = "nova_senha" e salvar. O sistema atualizará a senha instantaneamente sem precisar alterar nenhuma linha de código!
