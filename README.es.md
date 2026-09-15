# 🛡️ MonsterGet Skills — Web Scraping Anti-Bloqueo para IA

> **Deja de ser bloqueado. Extrae datos de TikTok desde tu navegador real — tu sesión ya iniciada. Automatizado por IA, cero configuración, permanentemente gratis.**

[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · **Español** · [Português](README.pt.md)

[![Gratis](https://img.shields.io/badge/🆓-Permanentemente%20Gratis-22bb33?style=flat-square)](https://monsterget.com)
[![IA Nativo](https://img.shields.io/badge/🤖-IA%20Nativo-2196F3?style=flat-square)](https://monsterget.com)
[![10M créditos](https://img.shields.io/badge/📦-10M%20al%20registrarse-FF9800?style=flat-square)](https://monsterget.com)

---

## ✨ ¿Qué es?

**MonsterGet Skills** convierte a cualquier asistente de IA en un motor de datos de TikTok — sin que tus cuentas sean bloqueadas.

Aquí está el secreto a voces del web scraping: **los scrapers del lado del servidor son bloqueados.** TikTok, Instagram, LinkedIn — todos luchan contra navegadores headless, IPs de datacenter y pools de proxies. Tú refuerzas, ellos bloquean más fuerte. Es una carrera armamentista que pierdes.

MonsterGet cambia el juego: **la extracción se ejecuta dentro de tu propio navegador**, en tu sesión real iniciada. TikTok ve a un usuario real. Tú obtienes los datos.

| Enfoque | Anti-bloqueo | Configuración | Costo |
|---------|-------------|---------------|-------|
| ❌ Scraper servidor | ❌ Bloqueado | Horas de config | Proxies + infra |
| ❌ Navegador headless | ❌ Detectado rápido | Selenium/Playwright | Facturas de servidor |
| ✅ **MonsterGet (tu navegador)** | ✅ **Invisible** | **2 minutos, una vez** | **🆓 Gratis: 10M entradas** |

## 🚀 ¿Qué puedes hacer?

| Caso de uso | Datos que obtienes |
|-------------|-------------------|
| 🔍 **Descubrimiento de influencers** | Busca creadores por palabra clave → CSV con bio, seguidores, avatar |
| 🎬 **Investigación de videos** | Busca videos por palabra clave → CSV con reproducciones, likes, comentarios, URL |
| 🏷️ **Inteligencia de hashtags** | Ingresa un hashtag → CSV de cada video bajo ese tag |
| 👤 **Auditoría de creadores** | Obtén todos los videos de un creador → análisis completo |
| 📊 **Perfiles masivos** | 50+ usuarios a la vez → un CSV agregado |

Todos los resultados son archivos CSV limpios — ábrelos en Excel, impórtalos a tu analizador, o alimenta a tu IA.

## 🤖 Diseño nativo para IA

Funciona con **todas** las herramientas de IA principales:

`Claude Code` · `Codex CLI` · `Cursor` · `Windsurf` · `Cline` · `Roo Code` · `Kilo Code` · `Copilot` · `Gemini CLI` · `Zed` · `Aider` · `Continue` · `Junie` · `Warp` · `Devin`

Este skill es **independiente del agente**: todo el trabajo de shell se delega en scripts protocolizados que emiten JSON, por lo que se comporta igual con Claude Code que con cualquier otra herramienta.

La IA orquesta todo:

```
🧠 IA: "Necesito datos de TikTok para investigación de mercado"
   ↓
🔗 Abre una URL en TU navegador
   ↓
🌐 Tu sesión real de TikTok + extensión MonsterGet recolectan los datos
   ↓
📥 La IA descarga el CSV y te lo entrega
```

**Nunca tocas Python, Selenium, proxies ni captchas.** La IA hace la orquestación, tu navegador hace el scraping.

## 🎁 Precios que tienen sentido

| Plan | Créditos | Ventanas concurrentes | Precio |
|------|----------|----------------------|--------|
| Gratis | **10,000,000** entradas | 1 | **🆓 $0 — permanentemente** |
| Miembro | Más | Más paralelo | Razonable |

Sin trampas. Sin "gratis por 14 días". 10 millones de entradas son reales.

## 💬 Lo que dicen los usuarios

> *"Rotaba 50 proxies y seguía siendo bloqueado en TikTok. MonsterGet funciona — la primera vez, siempre."*
> — **Analista de datos de e-commerce**

> *"Le dije a mi Claude 'encuentra 200 creadores de TikTok en belleza'. Volvió 3 minutos después con un CSV. No escribí ni una línea de código."*
> — **Dueño de agencia de marketing**

> *"La configuración tomó 2 minutos. He extraído 2 millones de entradas. Sigo en el plan gratis. Esto se siente ilegal pero aparentemente está bien."*
> — **Growth hacker**

## ⏱️ Configuración inicial — 2 minutos, una sola vez

| Paso | Qué hacer |
|------|-----------|
| 1 | [Regístrate gratis](https://monsterget.com) — email + contraseña, listo |
| 2 | [Instala la extensión](https://monsterget.com/install) — Chrome/Edge, 1 clic |
| 3 | Copia la carpeta del skill a tu cliente de IA → terminaste |

Después de eso, **cada extracción es instantánea.** Nunca más configuración.

## 📦 Skills disponibles

| Skill | Qué hace | Plataformas |
|-------|----------|-------------|
| [🎵 tiktok-collector](tiktok-collector/SKILL.md) | Búsqueda de videos TikTok, descubrimiento de creadores, colección de hashtags, perfiles de creador a CSV | TikTok |

*Más plataformas próximamente (LinkedIn, Instagram, X/Twitter, YouTube…). Abre un issue para votar.*

## 🔧 Cómo instalar

**Sin comandos que memorizar.** Abre tu asistente de IA (Claude Code / Codex / Cline…), y envía esto en el chat:

> 💬 Instala el skill tiktok-collector desde https://github.com/monsterget-com/skills

La IA clonará el repositorio, instalará el runtime y se configurará a sí misma.

### Lo que hace la IA

1. Clona el repositorio
2. Copia `tiktok-collector/` → `~/.monsterget/skill/` — un **directorio de runtime compartido**
3. Añade un puntero de una línea a su propio archivo de instrucciones personalizadas

Como el runtime vive en una ubicación fija (`~/.monsterget/skill/`), **todos tus clientes de IA lo comparten**. Instálalo una vez y úsalo desde Claude Code, Codex, Cursor, Cline — lo que tengas.

**¿Prefieres hacerlo a mano?** Consulta [tiktok-collector/INSTALL.md](tiktok-collector/INSTALL.md) para los pasos manuales y las ubicaciones de puntero por cliente.

**¿Sin acceso a shell** (solo chat web como ChatGPT)? Pega el contenido de [`tiktok-collector/SKILL.md`](tiktok-collector/SKILL.md) en tus instrucciones personalizadas — la IA te guiará manualmente.

## 🧠 Arquitectura (lo que realmente sucede)

```
IA ──▶ genera taskId + abre URL en el navegador
         │
Tu navegador ──▶ La extensión MonsterGet ejecuta la extracción en tu pestaña de TikTok
                   │
                Las filas se transmiten al buffer del servidor ──▶ IA consulta y descarga CSV
```

**No se almacenan datos en servidores después de la entrega.** Privacidad primero.

## 📄 Licencia

MIT — ver [LICENSE](LICENSE).

---

> **¿Listo para dejar de luchar contra sistemas anti-bot?** [Regístrate gratis →](https://monsterget.com)
>
> *10 millones de entradas. Una sesión de navegador. Cero cuentas bloqueadas.*