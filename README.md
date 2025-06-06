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