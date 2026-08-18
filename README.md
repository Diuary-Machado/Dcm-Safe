# DCM Safe 🛡️

> Sistema de cofre financeiro pessoal desenvolvido com foco em privacidade, segurança de dados e uma interface moderna em Dark Glassmorphism.

---

## ⚙️ Tecnologias

- **Python** (Lógica e backend)
- **Streamlit** (Interface web reativa)
- **SQLite** (Persistência de dados leve e local)
- **Pandas** (Processamento e análise de dados financeiros)
- **CSS Personalizado** (Design system customizado Dracula/Grey com tipografia moderna)

---

## 🚀 Funcionalidades

- **Autenticação Segura:** Cofre protegido por senha com controle de acesso local.
- **Gestão de Lançamentos:** Controle ágil de entradas, saídas e categorias financeiras.
- **Despesas Fixas:** Gerenciamento centralizado de compromissos recorrentes.
- **Dashboard Analítico:** Métricas consolidadas e visão geral do período.
- **Fechamento de Mês:** Ferramentas de auditoria, limpeza e consolidação de ciclos financeiros.

---

## 📂 Estrutura do Projeto

```text
DCM-SAFE/
├── app.py              # Ponto de entrada da aplicação Streamlit
├── auth.py             # Lógica de controle de acesso e autenticação
├── database.py         # Gerenciamento de conexões e queries do banco
├── styles.py           # Definição do design system e estilos CSS
├── requirements.txt    # Dependências do projeto
└── views/              # Módulos de telas da aplicação
    ├── dashboard.py
    ├── lancamentos.py
    ├── gerenciar.py
    └── fechamento.py
