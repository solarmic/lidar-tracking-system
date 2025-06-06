# 🎭 Sistema de Seguimiento Escénico con LIDAR

Este sistema detecta la posición de un actor en un escenario usando un sensor RPLIDAR A1, normaliza las coordenadas y las envía por UDP a Max Cycling para su uso en tiempo real en artes escénicas.

## ✨ Características Principales
- Detección de persona en movimiento
- Filtrado de ruido y objetos estáticos
- Normalización de coordenadas (0-1) con centro en (0.5,0.5)
- Comunicación UDP eficiente
- Reconexión automática en caso de fallos
- Modular y configurable

## 🖥️ Requisitos de Hardware
- Sensor RPLIDAR A1
- Raspberry Pi (o computador Mac para pruebas)
- Conexión USB

## 📂 Estructura del Proyecto
├── .vscode/
│ └── settings.json
├── src/
│ ├── init.py
│ ├── main.py
│ ├── lidar_processor.py
│ ├── position_tracker.py
│ └── udp_sender.py
├── requirements.txt
├── .gitignore
└── README.md

## ⚙️ Configuración Inicial

### Dependencias (requirements.txt)
rplidar-roboticia
numpy
pygame


### Instalación en Raspberry Pi
```bash
# Instalar dependencias del sistema
sudo apt-get update
sudo apt-get install libsdl2-2.0-0

# Dar permisos serial
sudo usermod -a -G dialout $USER
sudo reboot

# Clonar repositorio
git clone https://github.com/tu-usuario/lidar-tracking-system.git
cd lidar-tracking-system

# Crear entorno virtual e instalar dependencias
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Instalación en Mac
Instalar drivers CP210X: Descargar

Configurar entorno virtual:

git clone https://github.com/tu-usuario/lidar-tracking-system.git
cd lidar-tracking-system
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
