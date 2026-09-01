# RaspTranca — Tranca Automática Biométrica 🚪🔓

Projeto Integrador do **IFSC Campus Garopaba** — equipe **Petrus, Felipe e Martin ("Charlie")**.

Um sistema de **controle de acesso** para salas e laboratórios acadêmicos: uma tranca automática que substitui chaves físicas. O acesso é liberado pela leitura de um **código de barras** cadastrado para cada pessoa, com **saída de hardware no Raspberry Pi** (LEDs verde/vermelho) indicando liberado/negado.

Além do controle físico, o sistema tem uma **agenda de reserva de laboratórios** com **planilha visual de disponibilidade** (pública), login por usuário/senha e um **painel administrador** para gerenciar tudo.

---

## ✨ Funcionalidades

| Área | Descrição |
|---|---|
| 🏠 **Home (pública)** | Planilha visual de disponibilidade dos laboratórios: labs × períodos, célula verde = livre, vermelha = ocupada. Não precisa estar logado. |
| 🔐 **Login** | Acesso por email + senha (senhas com hash). Cadastro de novos usuários é feito **apenas pelo ADM**. |
| ⚙️ **Config** | Alterna modo claro/escuro, mostra a conta logada e dá acesso às funções de ADM quando o usuário é administrador. |
| 📅 **Agenda** | Usuário logado reserva um laboratório em um dos **8 períodos** do dia (padrão IFSC, 55 min cada). |
| 📋 **Minhas Reservas** | Usuário vê e cancela as próprias reservas. |
| 🛡️ **Painel ADM** | Dashboard + **Editor de Usuários** (nome, email, senha, código de barras, perfil admin) + **Editor de Laboratórios** + **todas as reservas**. |
| 🔎 **Verificação por código de barras** | Estação de acesso: passa o código de barras no leitor → valida no banco → acende LED verde (válido) ou vermelho (negado) no Raspberry Pi. |

### Períodos (padrão IFSC)
| Período | Horário |
|---|---|
| 1 | 08:00 - 08:55 |
| 2 | 09:00 - 09:50 |
| 3 | 10:10 - 11:05 |
| 4 | 11:10 - 12:00 |
| 5 | 13:30 - 14:25 |
| 6 | 14:30 - 15:20 |
| 7 | 15:40 - 16:35 |
| 8 | 19:00 - 19:55 |

---

## 🏗️ Estrutura do projeto

```
projeto-rasptraca/
├── README.md                  ← este arquivo
├── index.html                 ← landing page / relatório visual do projeto
├── documentacao/
│   └── PI - ... .pdf          ← documento oficial do PI
└── projeto rasptranca/        ← aplicação Flask
    ├── codigo.py              ← ponto de entrada (cria o app, inicia o banco)
    ├── routes.py              ← todas as rotas (home, login, agenda, admin, verificação)
    ├── banco_de_dados.py      ← conexão SQLite + schema + PERIODOS
    ├── usuarios.py            ← CRUD de usuários + login + verificação por código
    ├── agenda.py              ← CRUD de laboratórios e reservas + disponibilidade
    ├── autenticacao.py        ← decorators de login e de admin
    ├── rpi_luz.py             ← saída de hardware (LEDs GPIO) com fallback de simulação
    ├── banco.db               ← banco de dados SQLite
    ├── static/style.css       ← estilo (claro/escuro via CSS variables)
    └── templates/             ← páginas Jinja2
```

---

## 🚀 Como rodar

```bash
cd "projeto rasptranca"
python codigo.py
```

Acesse **http://127.0.0.1:5000**

> Dependências: **Flask** (e `gpiozero` opcional, apenas para o hardware do Raspberry Pi).

### Credenciais do administrador padrão

| Campo | Valor |
|---|---|
| Email | `admin@admin.com` |
| Senha | `admin127` |

O admin é criado automaticamente na primeira execução. **Troque a senha em produção.**

---

## 🧠 Por que estas tecnologias?

**Flask** — O sistema precisa de rotas simples (login, reservas, CRUD) e integração com hardware, sem a complexidade de um framework gigante. Flask é leve, fácil de ler/estender (ideal para um PI técnico) e roda em qualquer PC ou Raspberry Pi.

**SQLite** — Perguntas: "quantos usuários?" ou "quantas reservas por dia?". A resposta: poucos, num único laboratório. SQLite é um banco em arquivo único (`banco.db`), sem servidor, zero configuração — perfeito para o porte e para um protótipo que precisa subir rápido no Pi.

**Jinja2 (templates)** — Motor de templates padrão do Flask. Permite renderizar as listas de usuários, labs e períodos no HTML de forma organizada, sem misturar muita lógica no servidor.

**HTML/CSS/JS puros** — Sem frameworks front-end. O dark mode usa **CSS variables** + `localStorage` (guarda a preferência no navegador), sem necessidade de biblioteca externa. Mantém o projeto simples e autossuficiente.

**Raspberry Pi + gpiozero** — O Pi é barato, popular em escolas/técnicos e tem GPIO para controlar LEDs. A biblioteca `gpiozero` deixa o código de hardware curto e legível. O módulo `rpi_luz.py` usa `try/import`: no PC ele *simula* os LEDs (imprime no console), no Pi ele acende os LEDs reais — o mesmo código roda nos dois lugares.

**werkzeug (hash de senhas)** — Já acompanha o Flask. Senhas nunca são guardadas em texto puro, só o hash. É o mínimo de segurança aceitável para um protótipo com login.

---

## 🔒 Segurança (atual e a melhorar)

- ✅ Senhas com hash (`werkzeug.security`)
- ✅ Rotas de admin protegidas por decorator (`admin_required`)
- ⚠️ `SECRET_KEY` do Flask fixa no código (`codigo.py`) — em produção, use variável de ambiente
- ⚠️ Senha do admin padrão deve ser trocada
- ⚠️ Sem proteção `CSRF` — aceitável para protótipo/PI, mas deve entrar em produção

---

## 📍 Observação sobre a migração

O antigo modelo usava **leitura de digitais** (`Usuario`/`Digital`). Ele foi **substituído por código de barras** dentro de um único sistema de usuários (`SistemaUsuario`, com coluna `codigo_barras`). As tabelas antigas permanecem no arquivo `banco.db` sem uso — nada é apagado, para não perder dados históricos.