# Cronograma do Projeto IFMA - Automação Residencial

**Projeto:** Simulação de Automação Residencial com IoT no Cisco Packet Tracer  
**Instituição:** IFMA - Campus Monte Castelo  
**Período:** Abril - Maio 2026  
**Repositório:** [github.com/ccfernandes600/ifma-smart-home-packet-tracer](https://github.com/ccfernandes600/ifma-smart-home-packet-tracer)

---

## 📋 Visão Geral do Projeto

Desenvolvimento de uma infraestrutura completa de rede corporativa com automação residencial IoT, utilizando Cisco Packet Tracer 9.0.0. O projeto integra NAT, Frame Relay, servidores web (local e na nuvem), e lógica de segurança com 3 estados operacionais.

---

## 🎯 Fases do Projeto

### Fase 1: Infraestrutura de Rede ✅ **CONCLUÍDA**

**Período:** 30 de abril - 02 de maio  
**Status:** 100% completa

#### Objetivos
- [x] Configurar topologia de rede com 2 roteadores
- [x] Implementar NAT Overload (PAT) no Router0
- [x] Implementar NAT Estático 1:1 no Router1
- [x] Configurar Frame Relay via Cloud-PT
- [x] Estabelecer conectividade WAN entre sites

#### Realizações
- **Router0 (Site A - Automação)**
  - LAN: 192.168.1.0/24 (Gi0/0)
  - WAN: 200.0.0.1/29 (Se0/3/0)
  - NAT Overload configurado
  - Rota padrão para internet

- **Router1 (Site B - Servidor)**
  - WAN: 200.0.0.2/29 (Se0/3/0)
  - LAN: 10.0.0.0/24 (Gi0/0)
  - Static NAT 1:1 (10.0.0.10 ↔ 200.0.0.10)
  - Rota reversa para rede de automação

- **Frame Relay WAN**
  - Cloud-PT configurado
  - DLCI 102 (Router0 → Router1)
  - DLCI 201 (Router1 → Router0)
  - Mapeamentos estáticos funcionais

#### Desafios Superados
- ❌ Cable Modem e DSL Modem não funcionaram no PT 9.0.0
- ✅ Solução: Migração para portas seriais com Frame Relay
- ✅ Tempo investido: ~20% do projeto inicial

---

### Fase 2: Serviços e Aplicação ✅ **CONCLUÍDA**

**Período:** 02 de maio - 09 de maio  
**Status:** 100% completa

#### Objetivos
- [x] Desenvolver portal web para servidor interno
- [x] Publicar portal externo no Netlify
- [x] Configurar SBC Proxy Web
- [x] Integrar servidores com topologia

#### Realizações

**Servidor Interno (Packet Tracer)**
- Arquivo: `index_servidor_interno_V3_09_05.html`
- IP real: 10.0.0.10
- IP público NAT: 200.0.0.10
- Recursos:
  - Identidade visual IFMA (verde, vermelho, preto)
  - Status dos dispositivos IoT
  - Mapa de portas do SBC IoT
  - Tabelas de topologia
  - Fluxo NAT/WAN documentado
  - Relógio e uptime em tempo real

**Servidor Externo (Netlify)**
- Arquivo: `netlify-index_V3_09_05.html`
- URL: `https://ifma-automacao-packet-tracer.netlify.app/`
- Recursos:
  - Google Fonts (Rajdhani, Share Tech Mono, Exo 2)
  - Animações CSS avançadas
  - Grid animado do logo IFMA
  - Design responsivo
  - Meta tags SEO
  - Relógio e contador de uptime

**SBC Proxy Web**
- IP: 192.168.1.50
- Função: Buscar página do Netlify e entregar ao PC0
- Permite acesso ao portal externo sem sair da LAN

#### Desafios Superados
- ✅ Integração servidor interno + externo + proxy
- ✅ Design profissional com identidade IFMA
- ✅ Documentação completa em ambos portais

---

### Fase 3: Lógica IoT e Segurança ✅ **CONCLUÍDA**

**Período:** 30 de abril - 09 de maio  
**Status:** 100% completa

#### Objetivos
- [x] Implementar lógica de automação em Python
- [x] Configurar sensores e atuadores
- [x] Criar sistema de 3 estados de segurança
- [x] Implementar LED RGB como indicador visual
- [x] Configurar LCD para feedback textual

#### Realizações

**Hardware IoT - SBC IoT (192.168.1.20)**

| Porta | Dispositivo | API | Função |
|-------|-------------|-----|--------|
| D0 | Sensor de Movimento | `digitalRead/Write` | Detecção PIR |
| D1 | Porta de Garagem | `customRead/Write` | IoT3 - Garagem |
| D2 | Porta Principal | `customRead/Write` | IoT1 - Entrada |
| D3 | Janela | `customRead/Write` | IoT2 - Janela |
| D4 | Câmera | `customRead/Write` | Webcam 01 |
| D5 | Sirene | `customRead/Write` | IoT8 - Alarme |
| D6 | LCD Display | `customRead/Write` | IoT0 - 2 linhas |
| D7 | LED R (Vermelho) | `analogRead/Write` | Canal R do RGB |
| D8 | LED G (Verde) | `analogRead/Write` | Canal G do RGB |
| D9 | LED B (Azul) | `analogRead/Write` | Canal B do RGB |

**Lógica de Segurança (3 Estados)**

1. **NORMAL** (Verde: 0, 900, 0)
   - Nenhum sensor ativado
   - Câmera e sirene desligadas
   - LCD: "SISTEMA SEGURO / ESTADO NORMAL"

2. **MONITORAMENTO** (Laranja: 1023, 512, 0)
   - Movimento OU abertura (não ambos)
   - Câmera ativada, sirene desligada
   - LCD: "MONITORAMENTO / MOV. DETECTADO" ou "ABERTO: \<setor\>"

3. **ALERTA** (Vermelho: 1023, 0, 0)
   - Movimento E abertura simultâneos
   - Câmera e sirene ativadas
   - LCD: "ALERTA VIOLACAO / SETOR: \<setor\>"

**Código Python**
- Arquivo: `main.py`
- Versão estável e testada
- Lógica incremental (evoluiu de teste 01 até teste 06)
- Estrutura modular com funções dedicadas

#### Desafios Superados
- ❌ MCU com portas analógicas NÃO funcionava no PT 9.0.0
- ❌ Dezenas de iterações de código sem sucesso
- ✅ **Solução**: Migração para SBC IoT (portas digitais)
- ✅ Sucesso imediato após mudança de hardware
- ⏱️ **Tempo investido**: ~40% do projeto total

---

### Fase 4: Documentação Técnica ✅ **CONCLUÍDA**

**Período:** 09 de maio  
**Status:** 100% completa

#### Objetivos
- [x] Criar repositório GitHub
- [x] Escrever README.md completo
- [x] Documentar topologia de rede
- [x] Mapear portas e dispositivos
- [x] Explicar lógica de automação
- [x] Documentar uso de IA no desenvolvimento

#### Realizações

**Repositório GitHub**
- Nome: `ifma-smart-home-packet-tracer`
- Licença: MIT
- Descrição completa
- Arquivos organizados:
  - `README.md` (documentação principal)
  - `main.py` (código IoT)
  - `index_servidor_interno_V3_09_05.html`
  - `netlify-index_V3_09_05.html`
  - `Topologia atualizada v3_09_05.png`
  - `diagrama_rede_v3.svg` / `.png` (topologia vetorial)
  - `og-image.svg` / `.png` (preview Open Graph)
  - `LICENSE` (MIT)

**README.md - Estrutura**
1. Objetivos do Projeto
2. Topologia de Rede (com imagem)
3. Núcleo IoT – SBC IoT
4. Lógica de Operação (3 estados)
5. Portal Web Dual (interno + externo)
6. Estrutura do Repositório
7. Como Reproduzir no Cisco Packet Tracer
8. **Uso de Inteligência Artificial no Desenvolvimento**
   - 8.1 Ferramentas Utilizadas
   - 8.2 Desafios Técnicos Encontrados
   - 8.3 Fluxo de Trabalho com IA
   - 8.4 Lições Aprendidas
9. Tecnologias Utilizadas
10. Licença

**Documentação do Uso de IA**
- Claude AI (versão básica): configuração inicial
- Perplexity Pro + Claude Sonnet 4.6: desenvolvimento principal
- Google Gemini Pro: validação de código
- Transparência sobre autoria e controle humano
- Registro de 40% do tempo em debugging do PT

#### Desafios Superados
- ✅ Organização clara de seções
- ✅ Formatação consistente em Markdown
- ✅ Inserção de imagem com espaços no nome (`%20`)
- ✅ Correção manual da ordem das seções 8 e 9

---

### Fase 5: Publicação e Portfólio 🔄 **EM ANDAMENTO**

**Período:** Junho de 2026  
**Status:** Em preparação

#### Objetivos
- [x] Revisar e limpar repositório GitHub
- [ ] Preparar post para LinkedIn
- [ ] Adicionar ao portfólio/currículo

#### Plano de Ação

**LinkedIn (Prioridade 1)**
- Resumo executivo do projeto (300-500 palavras)
- Destaques: NAT, Frame Relay, IoT, Python, IA
- Links: repositório GitHub + portal Netlify ao vivo
- Hashtags: #Redes #IoT #CiscoPacketTracer #IFMA #Python

---

## 📊 Cronograma Temporal

### Abril 2026
- **30/04**: Início do projeto com Claude AI
  - Configuração inicial dos roteadores
  - Primeiras tentativas com Cable/DSL Modem
  - Decisão de usar Frame Relay

### Maio 2026
- **01/05**: Migração para Frame Relay
  - Cloud-PT configurado com sucesso
  - NAT básico funcionando
  
- **02/05**: Finalização da rede WAN
  - Static NAT 1:1 implementado
  - IP público dedicado (200.0.0.10)
  - Primeiras versões dos portais HTML
  - Fim do período gratuito do Claude

- **03-08/05**: Desenvolvimento IoT e debugging
  - Migração para Perplexity + Claude Sonnet 4.6
  - Múltiplas iterações com MCU (sem sucesso)
  - Validação com Gemini Pro
  - Descoberta do bug das portas analógicas
  - Migração para SBC IoT

- **09/05**: Documentação e finalização
  - README.md completo
  - Seção de uso de IA adicionada
  - Correções manuais finais
  - Portais HTML V3 finalizados

- **10/05–09/06**: Pausa no projeto
- **22/06**: Retomada — revisão geral, limpeza do repositório, preparação para publicação

---

## 📈 Distribuição de Tempo

| Atividade | Tempo Investido | % do Total |
|-----------|-----------------|------------|
| Debugging do Packet Tracer | ~40% | Bug MCU analógico |
| Configuração de rede | ~25% | NAT, Frame Relay, Cloud-PT |
| Desenvolvimento IoT | ~20% | Código Python, lógica |
| Portais web | ~10% | HTML interno e externo |
| Documentação | ~5% | README, organização |

---

## 🎓 Aprendizados e Conquistas

### Técnicos
1. ✅ Domínio de NAT Overload e Static NAT
2. ✅ Configuração de Frame Relay em Cloud-PT
3. ✅ Integração de servidores internos e externos
4. ✅ Programação em MicroPython para IoT
5. ✅ Debugging avançado de simuladores

### Soft Skills
1. ✅ Persistência na resolução de problemas (40% em debugging)
2. ✅ Migração entre ferramentas de IA mantendo contexto
3. ✅ Documentação técnica profissional
4. ✅ Gestão de projeto e cronograma
5. ✅ Transparência sobre uso de IA

### Descobertas Importantes
1. 🐛 Bug do Packet Tracer 9.0.0: portas analógicas da MCU não funcionam
2. 🐛 Cable Modem e DSL Modem não operam corretamente no PT 9 (Linux/Windows)
3. ✅ SBC IoT com portas digitais é mais confiável que MCU
4. ✅ Frame Relay via Cloud-PT é estável e funcional
5. ✅ Netlify é excelente para hospedar portais estáticos

---

## 📝 Notas Importantes

### Decisões de Projeto
- **MCU → SBC IoT**: Mudança crucial para o sucesso
- **Cable/DSL → Frame Relay**: Solução definitiva para WAN
- **IP dedicado 200.0.0.10**: Separação clara NAT vs roteamento
- **Dual portal**: Interno (PT) + Externo (Netlify)

### Ferramentas de IA Utilizadas
1. **Claude AI (básica)**: Configuração inicial (30/04 - 02/05)
2. **Perplexity Pro + Claude Sonnet 4.6**: Desenvolvimento principal (03/05 - 09/05)
3. **Google Gemini Pro**: Validação de código

### Controle e Autoria
- **Concepção**: 100% humana
- **Código**: 100% gerado por IA (sob direção humana)
- **Decisões técnicas**: Debatidas com IA, aprovadas pelo autor
- **Topologia**: Totalmente definida pelo autor
- **Comando do projeto**: Sempre nas mãos do desenvolvedor

---

## 🏆 Conclusão

Projeto completo e funcional que demonstra:
- Competência em redes (NAT, Frame Relay, roteamento)
- Habilidades de programação (Python/MicroPython)
- Capacidade de debugging e resolução de problemas
- Uso eficiente de ferramentas de IA
- Documentação técnica profissional
- Persistência e adaptabilidade

**Status Final:** Pronto para portfólio e divulgação profissional! 🎓🚀

---

*Documento gerado em: 09 de maio de 2026 · Atualizado em: 22 de junho de 2026*  
*Autor: Claudio Fernandes*  
*Instituição: IFMA - Campus Monte Castelo*