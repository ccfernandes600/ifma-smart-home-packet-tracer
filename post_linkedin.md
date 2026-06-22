# Post LinkedIn — Projeto Automação Residencial IoT (IFMA)

> Texto final para publicação. Anexar a imagem `infografico_linkedin.png` ao post.
> Hashtags enxugadas para 5 (recomendado no LinkedIn).

---

🏠🔐 **De um bug que consumiu 40% do projeto a um sistema de automação residencial funcionando: o que aprendi construindo redes no Cisco Packet Tracer.**

Como professor de **Introdução à Programação** e de **Técnicas de Programação aplicadas à Engenharia** no IFMA – Campus Monte Castelo. Gosto de levar para a sala projetos que unem teoria e prática real. Este é um deles.

Desenvolvi uma **infraestrutura de rede corporativa completa** com automação residencial IoT, integrando dois sites via WAN. O resultado:

🔹 **NAT Overload + NAT Estático 1:1** para acesso externo a um servidor com IP público dedicado
🔹 **Frame Relay** via Cloud-PT interligando a rede de automação (192.168.1.0/24) à rede de servidores (10.0.0.0/24)
🔹 **Núcleo IoT em Python** (SBC) com sensores de movimento, porta, janela e garagem
🔹 **Lógica de segurança em 3 estados** — NORMAL, MONITORAMENTO e ALERTA — com feedback em LED RGB (PWM), painel LCD e sirene
🔹 **Portal web duplo**: servidor interno na rede simulada + portal externo no Netlify, acessado via proxy SBC

Mas o aprendizado mais valioso não foi técnico — foi de **persistência**.

Passei cerca de **40% do tempo** depurando o que eu achava ser meu código. Dezenas de iterações. Até descobrir que o problema era um **bug do próprio Packet Tracer 9.0.0**: as portas analógicas da MCU simplesmente não respondiam. A solução foi migrar para um SBC com portas digitais — e tudo funcionou de imediato.

A lição que levo para meus alunos: **nem sempre o código está errado.** Saber distinguir "meu erro" de "limitação da ferramenta" é uma habilidade de engenharia tão importante quanto programar.

🤖 **Sobre o uso de IA:** fui transparente em toda a documentação. O código foi desenvolvido com auxílio de IA, mas a **concepção, a arquitetura, a topologia e todas as decisões técnicas foram 100% minhas**. A IA foi assistente — o comando do projeto sempre esteve nas minhas mãos. Ensinar a usar IA com responsabilidade é parte do nosso papel como educadores.

📂 Código, topologia e documentação completa no GitHub:
👉 https://github.com/ccfernandes600/ifma-smart-home-packet-tracer

🌐 Portal do projeto ao vivo:
👉 https://ifma-automacao-packet-tracer.netlify.app/

E você, como lida com o limite entre "erro meu" e "limitação da ferramenta" nos seus projetos? 👇

#CiscoPacketTracer #IoT #IFMA #Python #Redes

---

## Checklist de publicação
1. Anexar `infografico_linkedin.png` (1600×2400).
2. Horário sugerido: terça a quinta, 8h–10h ou ~12h.
3. Conferir se a 1ª linha (gancho) aparece antes do "...ver mais".
