# Projeto IFMA – Automação Residencial em Cisco Packet Tracer

Simulação de automação residencial com IoT, NAT, Frame Relay e SBC no Cisco Packet Tracer. Sensores, LED RGB, LCD e lógica de segurança em 3 estados: NORMAL, MONITORAMENTO e ALERTA.

---

## 1. Objetivos do Projeto

- Simular uma **infraestrutura de rede corporativa** com acesso externo via internet, NAT e Frame Relay.
- Integrar um **servidor de serviços** (DNS, Web, ICMP, Email) acessível com IP público.
- Implementar um **sistema de automação residencial** com sensores (movimento, porta, janela, garagem) e atuadores (câmera, sirene, LED RGB, LCD).
- Aplicar uma **lógica de segurança em três estados** (NORMAL, MONITORAMENTO, ALERTA), com feedback visual e textual.
- Publicar o resultado em servidor web local e em portal hospedado (Netlify).

---

## 2. Topologia de Rede

### LAN – 192.168.1.0/24

| Dispositivo     | IP              | Função                          |
|-----------------|-----------------|----------------------------------|
| PC0             | 192.168.1.10    | Estação de trabalho              |
| SBC0            | 192.168.1.20    | Núcleo IoT (automação)           |
| SBC Proxy Web   | 192.168.1.50    | Proxy HTTP interno               |
| Router0 (Gi0/0) | 192.168.1.1/24  | Gateway da LAN                   |

### WAN – Frame Relay via Cloud-PT

| Dispositivo        | IP WAN           | Função                        |
|--------------------|------------------|--------------------------------|
| Router0 (Se0/3/0)  | 200.0.0.1/29     | Lado LAN do backbone WAN       |
| Router1 (Se0/3/0)  | 200.0.0.2/29     | Lado servidor do backbone WAN  |

### DMZ / Servidor – 10.0.0.0/24

| Dispositivo        | IP               | Função                              |
|--------------------|------------------|--------------------------------------|
| Router1 (Gi0/0)    | 10.0.0.1/24      | Gateway da rede do servidor          |
| Server0            | 10.0.0.10/24     | Servidor de serviços (DNS, Web, Email, ICMP) |
| IP Público NAT 1:1 | 200.0.0.10       | Acesso externo ao Server0            |

---

## 3. Núcleo IoT – SBC0

O microcontrolador inicial (MCU) foi substituído pelo **SBC0** devido a um bug nas portas analógicas da MCU no Cisco Packet Tracer: mesmo utilizando corretamente as diretivas `analogWrite` e `analogRead`, as conexões analógicas da MCU simplesmente não funcionavam. Ao testar com o SBC, todas as portas passaram a operar corretamente.

### 3.1 Mapa de Portas da SBC0

**Portas Digitais (D0–D6)**

| Porta | Dispositivo           | API utilizada                     |
|-------|-----------------------|------------------------------------|
| D0    | Sensor de Movimento   | `digitalRead` / `digitalWrite`    |
| D1    | Sensor de Garagem     | `customRead` / `customWrite`      |
| D2    | Sensor de Porta       | `customRead` / `customWrite`      |
| D3    | Sensor de Janela      | `customRead` / `customWrite`      |
| D4    | Câmera                | `customRead` / `customWrite`      |
| D5    | Sirene                | `customRead` / `customWrite`      |
| D6    | Painel LCD (2 linhas) | `customRead` / `customWrite`      |

**Portas Analógicas – LED RGB (D7–D9)**

| Porta | Canal LED RGB   | API utilizada                  |
|-------|-----------------|--------------------------------|
| D7    | LED R (vermelho)| `analogWrite` / `analogRead`  |
| D8    | LED G (verde)   | `analogWrite` / `analogRead`  |
| D9    | LED B (azul)    | `analogWrite` / `analogRead`  |

> **Observação:** O LED RGB opera conectado a portas digitais do SBC, que internamente suportam PWM via `analogWrite`. A escala aceita é de **0 a 1023**, onde 1023 equivale ao brilho máximo (255 no padrão RGB tradicional).

---

## 4. Lógica de Segurança e Automação

Toda a lógica está implementada no arquivo `main.py` rodando na SBC0.

### 4.1 Presets de Cor do LED RGB

| Estado          | Cor      | R    | G   | B |
|-----------------|----------|------|-----|---|
| NORMAL          | Verde    | 0    | 900 | 0 |
| MONITORAMENTO   | Laranja  | 1023 | 512 | 0 |
| ALERTA          | Vermelho | 1023 | 0   | 0 |

### 4.2 Estados de Operação

| Estado        | Condição                          | Câmera | Sirene | LED      | LCD (linha 1 / linha 2)              |
|---------------|-----------------------------------|--------|--------|----------|--------------------------------------|
| NORMAL        | Sem movimento e sem abertura      | OFF    | OFF    | Verde    | `SISTEMA SEGURO` / `ESTADO NORMAL`  |
| MONITORAMENTO | Movimento OU abertura (não ambos) | ON     | OFF    | Laranja  | `MONITORAMENTO` / `MOV. DETECTADO` ou `ABERTO: <setor>` |
| ALERTA        | Movimento E abertura simultâneos  | ON     | ON     | Vermelho | `ALERTA VIOLACAO` / `SETOR: <setor>` |

### 4.3 Funcionamento das Interrupções

O sistema utiliza `add_event_detect()` para resposta imediata a qualquer mudança nos sensores:

```python
add_event_detect(SENSOR_MOV, processar_sistema)
add_event_detect(GARAGEM,    processar_sistema)
add_event_detect(PORTA,      processar_sistema)
add_event_detect(JANELA,     processar_sistema)
```

Qualquer alteração em D0–D3 dispara automaticamente a função `processar_sistema()`, que reavalia todos os sensores, decide o estado e atualiza câmera, sirene, LED RGB e LCD de forma sincronizada.

### 4.4 Redundância: LCD + Terminal

As mensagens exibidas no painel LCD são **espelhadas no terminal** com timestamp:

```
[Sat May 09 20:00:00 2026] ALERTA VIOLACAO | SETOR: PORTA
[Sat May 09 20:01:05 2026] MONITORAMENTO | MOV. DETECTADO
[Sat May 09 20:02:10 2026] SISTEMA SEGURO | ESTADO NORMAL
```

---

## 5. Fluxo de Comunicação

### 5.1 Acesso ao Servidor Web

```
PC0 (192.168.1.10)
  └─► Router0 LAN (192.168.1.1)
        └─► Router0 WAN (200.0.0.1) ──[Frame Relay]──► Router1 WAN (200.0.0.2)
              └─► NAT 1:1: 200.0.0.10 → 10.0.0.10
                    └─► Server0 (DNS / Web / Email / ICMP)
```

### 5.2 Fluxo de Eventos IoT

```
Sensor muda de estado
  └─► add_event_detect() dispara processar_sistema()
        └─► ler_sensores() → mov, abertura, setor
              └─► Decide estado (NORMAL / MONITORAMENTO / ALERTA)
                    ├─► analogWrite() → LED RGB
                    ├─► customWrite() → LCD
                    ├─► customWrite() → Câmera
                    ├─► customWrite() → Sirene
                    └─► print() → Terminal (log com timestamp)
```

---

## 6. Estrutura do Repositório

```
ifma-smart-home-packet-tracer/
├── main.py                  # Código da SBC0 – lógica de segurança IoT
├── README.md                # Documentação técnica do projeto
└── LICENSE                  # Licença MIT
```

---

## 7. Como Reproduzir no Cisco Packet Tracer

1. Abra o Cisco Packet Tracer (versão 9.0.0 ou superior).
2. Monte a topologia conforme o mapa de endereçamento da Seção 2.
3. Configure NAT Overload no Router0 e NAT estático 1:1 no Router1.
4. Configure o Frame Relay na Cloud-PT interligando Router0 e Router1.
5. Adicione um SBC ao Switch0 e conecte os dispositivos IoT nas portas D0–D9.
6. Cole o conteúdo de `main.py` no editor Python do SBC0.
7. Execute o script e teste acionando os sensores.

---

## 8. Tecnologias Utilizadas

- Cisco Packet Tracer 9.0.0
- Python (MicroPython para SBC/MCU no PT)
- NAT Overload e NAT Estático 1:1
- Frame Relay (Cloud-PT)
- Protocolo HTTP (servidor web local)
- LED RGB, Painel LCD, Sirene, Câmera (IoT PT)

---

## 9. Licença

Este projeto está licenciado sob a licença **MIT**. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---

> Projeto desenvolvido como atividade prática de Redes de Computadores e IoT – IFMA.

---

## 10. Código Python – main.py (SBC0)

```python
from gpio import *
from time import *

# --- CONFIGURAÇÃO DE CORES DO LED RGB ---
# Escala de 0 a 1023 conforme especificação do Packet Tracer
RGB_VERDE    = (0,    900, 0)      # Estado NORMAL
RGB_LARANJA  = (1023, 512, 0)      # Estado MONITORAMENTO
RGB_VERMELHO = (1023, 0,   0)      # Estado ALERTA

# --- MAPEAMENTO DAS PORTAS DO SBC0 ---
SENSOR_MOV = 0  # D0 - Sensor de Movimento  (digitalRead)
GARAGEM    = 1  # D1 - Garagem              (customRead)
PORTA      = 2  # D2 - Porta                (customRead)
JANELA     = 3  # D3 - Janela               (customRead)
CAMERA     = 4  # D4 - Camera               (customWrite)
SIRENE     = 5  # D5 - Sirene               (customWrite)
LCD_PANEL  = 6  # D6 - Painel LCD           (customWrite)
LED_R      = 7  # D7 - LED Vermelho         (analogWrite)
LED_G      = 8  # D8 - LED Verde            (analogWrite)
LED_B      = 9  # D9 - LED Azul             (analogWrite)

def aplicar_rgb(cor_tuple):
    r, g, b = cor_tuple
    analogWrite(LED_R, r)
    analogWrite(LED_G, g)
    analogWrite(LED_B, b)

def ler_sensores():
    mov   = digitalRead(SENSOR_MOV) == HIGH
    g_raw = customRead(GARAGEM).strip()
    j_raw = customRead(JANELA).strip()
    p_raw = customRead(PORTA).strip()
    gar = (g_raw == "1")
    jan = (j_raw == "1")
    por = (len(p_raw) > 0 and p_raw[0] == "1")
    abertura = (gar or por or jan)
    setor = ""
    if gar:   setor = "GARAGEM"
    elif por: setor = "PORTA"
    elif jan: setor = "JANELA"
    return mov, abertura, setor

def processar_sistema(*args):
    movimento, abertura, setor = ler_sensores()
    agora = ctime()

    if abertura and movimento:
        customWrite(CAMERA, "1")
        customWrite(SIRENE, "1")
        aplicar_rgb(RGB_VERMELHO)
        msg = "ALERTA VIOLACAO\nSETOR: " + setor
        customWrite(LCD_PANEL, msg)
        print("[{}] {}".format(agora, msg.replace("\n", " | ")))

    elif abertura or movimento:
        customWrite(CAMERA, "1")
        customWrite(SIRENE, "0")
        aplicar_rgb(RGB_LARANJA)
        detalhe = "ABERTO: " + setor if abertura else "MOV. DETECTADO"
        msg = "MONITORAMENTO\n" + detalhe
        customWrite(LCD_PANEL, msg)
        print("[{}] {}".format(agora, msg.replace("\n", " | ")))

    else:
        customWrite(CAMERA, "0")
        customWrite(SIRENE, "0")
        aplicar_rgb(RGB_VERDE)
        msg = "SISTEMA SEGURO\nESTADO NORMAL"
        customWrite(LCD_PANEL, msg)
        print("[{}] {}".format(agora, msg.replace("\n", " | ")))

def setup():
    for p in [CAMERA, SIRENE, LCD_PANEL, LED_R, LED_G, LED_B]:
        pinMode(p, OUT)
    for p in [SENSOR_MOV, GARAGEM, PORTA, JANELA]:
        pinMode(p, IN)
    print("[{}] Sistema iniciado. Monitoramento ativo.".format(ctime()))
    processar_sistema()

def main():
    setup()
    add_event_detect(SENSOR_MOV, processar_sistema)
    add_event_detect(GARAGEM,    processar_sistema)
    add_event_detect(PORTA,      processar_sistema)
    add_event_detect(JANELA,     processar_sistema)
    while True:
        sleep(1)

if __name__ == "__main__":
    main()
```
