# DCM Safe 🛡️

> Um cofre financeiro pessoal de alta performance, desenvolvido com foco em privacidade absoluta, segurança de dados e uma experiência de usuário imersiva em **Dark Glassmorphism**.

---

## 🚀 Sobre o Projeto

O **DCM Safe** nasceu da necessidade de gerenciar finanças pessoais com total autonomia, sem depender de plataformas de terceiros que comercializam dados, unindo engenharia de software limpa, design moderno e uma arquitetura modular robusta.

---

## ⚙️ Stack Tecnológica

* **Backend & Lógica:** Python 3.x
* **Interface Web:** Streamlit (reativa, fluida e dinâmica)
* **Persistência de Dados:** SQLite (leve, local e segura)
* **Processamento de Dados:** Pandas
* **Design System:** CSS Customizado (Estética Dracula/Grey, tipografia moderna e efeitos de vidro fosco)

---

## ✨ Principais Funcionalidades

* 🔐 **Autenticação Segura:** Sistema de login com cofre protegido por senha, garantindo isolamento e privacidade total dos registros.
* 💸 **Gestão Dinâmica de Lançamentos:** Controle ágil de entradas, saídas, filtragem por categorias e listagem detalhada.
* 📌 **Controle de Despesas Fixas:** Gerenciamento centralizado de compromissos recorrentes mensais.
* 📊 **Dashboard Analítico:** Métricas consolidadas, indicadores de saldo e visão geral do período.
* 🔄 **Fechamento de Mês:** Ferramentas avançadas de auditoria, limpeza de dados e consolidação de ciclos financeiros.

---


## 📂 Arquitetura e Estrutura do Projeto

O projeto foi construído seguindo princípios de separação de responsabilidades e modularidade:

```text
DCM-SAFE/
├── app.py              # Ponto de entrada e roteador principal da aplicação Streamlit
├── auth.py             # Lógica de controle de acesso e autenticação de usuários
├── database.py         # Camada de persistência (conexões, criação de tabelas e queries SQL)
├── styles.py           # Design System (injeção de CSS customizado e componentes visuais)
├── requirements.txt    # Dependências e bibliotecas do projeto
└── views/              # Módulos de telas e visualizações da aplicação
    ├── dashboard.py    # Painel de métricas e gráficos consolidados
    ├── lancamentos.py  # Tela de registro de transações
    ├── gerenciar.py    # Gerenciamento e edição de despesas fixas/avulsas
    └── fechamento.py   # Auditoria e fechamento de ciclos mensais
## 🛠️ Como Executar Localmente

Siga os passos abaixo para clonar e rodar o projeto na sua máquina:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Diuary-Machado/Dcm-Safe.git
   ```

2. **Acesse o diretório do projeto:**
   ```bash
   cd Dcm-Safe
   ```

3. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   
   # No Windows:
   venv\Scripts\activate
   
   # No Linux/macOS:
   source venv/bin/activate
   ```

4. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Execute a aplicação:**
   ```bash
   streamlit run app.py
   ```

> *Nota: O banco de dados local (`finance.db`) e a estrutura de tabelas serão gerados automaticamente na primeira inicialização.*

---

## 👤 Autor

Desenvolvido por **Diuary Machado**.
