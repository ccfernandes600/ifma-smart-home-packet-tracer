from gpio import * # Biblioteca para controle de entrada e saída [cite: 15]
from time import * # Biblioteca para funções de tempo e log [cite: 23]

# --- 1. CONFIGURAÇÃO DE CORES (Escala 0-1023) ---
RGB_VERDE    = (0,    900, 0)
RGB_LARANJA  = (1023, 512, 0)
RGB_VERMELHO = (1023, 0,   0)

# --- 2. MAPEAMENTO DE HARDWARE (D0 - D9) ---
# Entradas (Sensores)
SENSOR_MOV = 0  # D0: Sensor de movimento digital
GARAGEM    = 1  # D1: Sensor customizado da garagem
PORTA      = 2  # D2: Sensor customizado da porta
JANELA     = 3  # D3: Sensor customizado da janela

# Saídas (Atuadores e Visual)
CAMERA     = 4  # D4: Atuador da Câmera
SIRENE     = 5  # D5: Atuador da Sirene
LCD_PANEL  = 6  # D6: Painel LCD (String)
LED_R      = 7  # D7: Canal Vermelho do LED RGB
LED_G      = 8  # D8: Canal Verde do LED RGB
LED_B      = 9  # D9: Canal Azul do LED RGB

def aplicar_rgb(cor_tuple):
    """ Envia sinais PWM (0-1023) para as portas digitais do LED RGB """
    r, g, b = cor_tuple
    analogWrite(LED_R, r)  # [cite: 15]
    analogWrite(LED_G, g)  # [cite: 15]
    analogWrite(LED_B, b)  # [cite: 15]

def ler_sensores():
    """ Lê e limpa os dados dos sensores para garantir lógica precisa """
    mov = digitalRead(SENSOR_MOV) == HIGH  # Lê nível lógico 0 ou 1 [cite: 15]
    
    # Limpeza de strings (strip) para evitar erros de comparação no Packet Tracer [cite: 5, 15]
    g_raw = customRead(GARAGEM).strip()
    j_raw = customRead(JANELA).strip()
    p_raw = customRead(PORTA).strip()
    
    gar = (g_raw == "1")
    jan = (j_raw == "1")
    # Captura o primeiro caractere para ignorar estados extras (ex: "1,0")
    por = (len(p_raw) > 0 and p_raw[0] == "1")
    
    abertura = (gar or por or jan)
    setor = "GARAGEM" if gar else "PORTA" if por else "JANELA" if jan else ""
    
    return mov, abertura, setor

def processar_sistema(*args):
    """ Lógica centralizada com sincronização LCD + Terminal """
    movimento, abertura, setor = ler_sensores()
    agora = ctime()  # Carimbo de tempo para o log do terminal [cite: 23]
    
    # --- ESTADO 1: VERMELHO (ALERTA MÁXIMO) ---
    # Ativação: Acesso aberto + Movimento detectado
    if abertura and movimento:
        msg1, msg2 = "ALERTA VIOLACAO", "SETOR: " + setor
        
        # Atuadores
        customWrite(CAMERA, "1")
        customWrite(SIRENE, "1")
        aplicar_rgb(RGB_VERMELHO)
        
        # Sincronização Redundante
        customWrite(LCD_PANEL, "{}\n{}".format(msg1, msg2))
        print("[{}] {} | {}".format(agora, msg1, msg2))

    # --- ESTADO 2: LARANJA (MONITORAMENTO) ---
    # Ativação: Apenas Abertura OU Apenas Movimento
    elif abertura or movimento:
        msg1 = "MONITORAMENTO"
        msg2 = "ABERTO: " + setor if abertura else "MOV. DETECTADO"
        
        # Atuadores
        customWrite(CAMERA, "1")
        customWrite(SIRENE, "0")  # Sirene desligada no monitoramento [cite: 4]
        aplicar_rgb(RGB_LARANJA)
        
        # Sincronização Redundante
        customWrite(LCD_PANEL, "{}\n{}".format(msg1, msg2))
        print("[{}] {} | {}".format(agora, msg1, msg2))

    # --- ESTADO 3: VERDE (NORMAL) ---
    # Ativação: Tudo fechado e sem movimento
    else:
        msg1, msg2 = "SISTEMA SEGURO", "ESTADO NORMAL"
        
        # Atuadores
        customWrite(CAMERA, "0")
        customWrite(SIRENE, "0")
        aplicar_rgb(RGB_VERDE)
        
        # Sincronização Redundante
        customWrite(LCD_PANEL, "{}\n{}".format(msg1, msg2))
        print("[{}] {} | {}".format(agora, msg1, msg2))

def setup():
    """ Configura os modos das portas no início do programa """
    # Portas de Saída (Controle)
    for p in [CAMERA, SIRENE, LCD_PANEL, LED_R, LED_G, LED_B]:
        pinMode(p, OUT)  # [cite: 15]
    
    # Portas de Entrada (Leitura)
    for p in [SENSOR_MOV, GARAGEM, PORTA, JANELA]:
        pinMode(p, IN)   # [cite: 15]
        
    print("[{}] Sistema Iniciado - Monitoramento Ativo.".format(ctime()))
    processar_sistema()

def main():
    setup()
    # Adição de interrupções para resposta instantânea a eventos [cite: 23]
    add_event_detect(SENSOR_MOV, processar_sistema)
    add_event_detect(GARAGEM,    processar_sistema)
    add_event_detect(PORTA,      processar_sistema)
    add_event_detect(JANELA,     processar_sistema)
    
    while True:
        sleep(1)  # Mantém o script rodando na MCU [cite: 23]

if __name__ == "__main__":
    main()