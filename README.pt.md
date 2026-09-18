# 🛡️ MonsterGet Skills — Web Scraping Anti-Bloqueio para IA

> **Pare de ser bloqueado. Extraia dados do TikTok através do seu navegador real — sua sessão já logada. Automatizado por IA, zero configuração, permanentemente grátis.**

[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [Español](README.es.md) · **Português**

[![Grátis](https://img.shields.io/badge/🆓-Permanentemente%20Grátis-22bb33?style=flat-square)](https://monsterget.com)
[![IA Nativo](https://img.shields.io/badge/🤖-IA%20Nativo-2196F3?style=flat-square)](https://monsterget.com)
[![10M créditos](https://img.shields.io/badge/📦-10M%20ao%20registrar-FF9800?style=flat-square)](https://monsterget.com)
[![Install via npx skills](https://img.shields.io/badge/🧩-Install%20via%20skills.sh-000?style=flat-square)](https://skills.sh)
[![Install via Claude Code](https://img.shields.io/badge/⚡-Install%20via%20Claude%20Code-6B46C1?style=flat-square)](https://github.com/monsterget-com/skills)

---

## ✨ O que é?

**MonsterGet Skills** transforma qualquer assistente de IA em uma potência de dados do TikTok — sem que suas contas sejam banidas.

Aqui está o segredo sujo do web scraping: **scrapers do lado do servidor são bloqueados.** TikTok, Instagram, LinkedIn — todos lutam contra navegadores headless, IPs de datacenter e pools de proxies. Você reforça, eles bloqueiam mais forte. É uma corrida armamentista que você perde.

MonsterGet vira o jogo: **a extração roda dentro do seu próprio navegador**, na sua sessão real logada. O TikTok vê um usuário real. Você recebe os dados.

| Abordagem | Anti-bloqueio | Configuração | Custo |
|-----------|--------------|--------------|-------|
| ❌ Scraper servidor | ❌ Bloqueado | Horas de config | Proxies + infra |
| ❌ Navegador headless | ❌ Detectado rápido | Selenium/Playwright | Contas de servidor |
| ✅ **MonsterGet (seu navegador)** | ✅ **Invisível** | **2 minutos, única vez** | **🆓 Grátis: 10M entradas** |

## 🚀 O que você pode fazer?

| Caso de uso | Dados que você obtém |
|-------------|---------------------|
| 🔍 **Descoberta de influenciadores** | Pesquise criadores por palavra-chave → CSV com bio, seguidores, avatar |
| 🎬 **Pesquisa de vídeos** | Pesquise vídeos por palavra-chave → CSV com plays, likes, comentários, URL |
| 🏷️ **Inteligência de hashtags** | Insira uma hashtag → CSV de cada vídeo sob ela |
| 👤 **Auditoria de criadores** | Obtenha todos os vídeos de um criador → análise completa |
| 📊 **Perfis em lote** | 50+ usuários de uma vez → um CSV agregado |

Todos os resultados são arquivos CSV limpos — abra no Excel, importe para sua ferramenta de análise, ou alimente sua IA.

## 🤖 Design nativo para IA

Funciona com **todas** as principais ferramentas de IA:

`Claude Code` · `Codex CLI` · `Cursor` · `Windsurf` · `Cline` · `Roo Code` · `Kilo Code` · `Copilot` · `Gemini CLI` · `Zed` · `Aider` · `Continue` · `Junie` · `Warp` · `Devin`

Este skill é **independente de agente**: todo o trabalho de shell é delegado a scripts protocolados que emitem JSON, então ele se comporta igualmente com Claude Code ou qualquer outra ferramenta.

A IA orquestra tudo:

```
🧠 IA: "Preciso de dados do TikTok para pesquisa de mercado"
   ↓
🔗 Abre uma URL no SEU navegador
   ↓
🌐 Sua sessão real do TikTok + extensão MonsterGet coletam os dados
   ↓
📥 IA baixa o CSV e entrega para você
```

**Você nunca toca em Python, Selenium, proxies ou captchas.** A IA faz a orquestração, seu navegador faz a extração.

## 🎁 Preços que realmente fazem sentido

| Plano | Créditos | Janelas concorrentes | Preço |
|-------|----------|---------------------|-------|
| Grátis | **10.000.000** entradas | 1 | **🆓 $0 — permanentemente** |
| Membro | Mais | Mais paralelo | Razoável |

Sem truques. Sem "grátis por 14 dias". 10 milhões de entradas são reais.

## 💬 O que os usuários dizem

> *"Eu rotacionava 50 proxies e ainda era bloqueado no TikTok. MonsterGet simplesmente funciona — na primeira vez, sempre."*
> — **Analista de dados de e-commerce**

> *"Falei para meu Claude 'encontre 200 criadores de TikTok na área de beleza'. Ele voltou 3 minutos depois com um CSV. Não escrevi uma única linha de código."*
> — **Dono de agência de marketing**

> *"A configuração levou 2 minutos. Já extraí 2 milhões de entradas. Ainda no plano grátis. Parece ilegal mas aparentemente está tudo bem."*
> — **Growth hacker**

## ⏱️ Configuração inicial — 2 minutos, única vez

| Passo | O que fazer |
|-------|-------------|
| 1 | [Registre-se grátis](https://monsterget.com) — email + senha, pronto |
| 2 | [Instale a extensão](https://monsterget.com/install) — Chrome/Edge, 1 clique |
| 3 | Copie a pasta do skill para seu cliente de IA → pronto |

Depois disso, **cada extração é instantânea.** Nunca mais configure.

## 📦 Skills disponíveis

| Skill | O que faz | Plataformas |
|-------|-----------|-------------|
| [🎵 tiktok-collector](skills/tiktok-collector/SKILL.md) | Pesquisa de vídeos TikTok, descoberta de criadores, coleta de hashtags, perfil de criador para CSV | TikTok |

*Mais plataformas em breve (LinkedIn, Instagram, X/Twitter, YouTube…). Abra uma issue para votar.*

## 🔧 Como instalar

**Sem comandos para decorar.** Abra seu assistente de IA (Claude Code / Codex / Cline…), e envie isto no chat:

> 💬 Instale o skill tiktok-collector de https://github.com/monsterget-com/skills

A IA clonará o repositório, instalará o runtime e se configurará.

### O que a IA faz

1. Clona o repositório
2. Copia `skills/tiktok-collector/` → `~/.monsterget/skill/` — um **diretório de runtime compartilhado**
3. Adiciona um ponteiro de uma linha ao seu próprio arquivo de instruções personalizadas

Como o runtime fica em um local fixo (`~/.monsterget/skill/`), **todos os seus clientes de IA o compartilham**. Instale uma vez e use com Claude Code, Codex, Cursor, Cline — o que você tiver.

**Prefere fazer manualmente?** Veja [skills/tiktok-collector/INSTALL.md](skills/tiktok-collector/INSTALL.md) para os passos manuais e os locais de ponteiro por cliente.

**Sem acesso ao shell** (chat só na web, como ChatGPT)? Cole o conteúdo de [`skills/tiktok-collector/SKILL.md`](skills/tiktok-collector/SKILL.md) nas instruções personalizadas — a IA vai guiá-lo manualmente.

## 🧠 Arquitetura (o que realmente acontece)

```
IA ──▶ gera taskId + abre URL no navegador
         │
Seu navegador ──▶ A extensão MonsterGet executa a extração na sua aba do TikTok
                   │
                Linhas são enviadas ao buffer do servidor ──▶ IA consulta e baixa CSV
```

**Nenhum dado é armazenado nos servidores após a entrega.** Privacidade em primeiro lugar.

## 📄 Licença

MIT — veja [LICENSE](LICENSE).

---

> **Pronto para parar de lutar contra sistemas anti-bot?** [Registre-se grátis →](https://monsterget.com)
>
> *10 milhões de entradas. Uma sessão de navegador. Zero contas bloqueadas.*