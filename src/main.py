import time
from .lidar_processor import LidarProcessor
from .position_tracker import PositionTracker
from .udp_sender import UDPSender

# Configuración
LIDAR_PORT = '/dev/ttyUSB0'  # '/dev/cu.SLAB_USBtoUART' en Mac
UDP_TARGET = ('127.0.0.1', 5000)  # Max Cycling
STAGE_SIZE = 6  # 6x6 metros
SCAN_INTERVAL = 0.1  # 100ms

def main():
    # Inicializar componentes
    lidar = LidarProcessor(LIDAR_PORT)
    tracker = PositionTracker()
    sender = UDPSender(*UDP_TARGET)
    
    previous_scan = None
    
    try:
        print("🚀 Sistema de seguimiento escénico iniciado")
        print(f"🏟️ Escenario: {STAGE_SIZE}x{STAGE_SIZE} metros")
        print(f"📡 Enviando datos a {UDP_TARGET[0]}:{UDP_TARGET[1]}")
        
        while True:
            # Capturar datos del LIDAR
            current_scan = lidar.capture_scan()
            
            # Filtrar objetivos móviles
            filtered_scan = lidar.filter_moving_targets(
                current_scan, 
                previous_scan
            )
            
            # Detectar posición
            position = tracker.detect_main_target(filtered_scan, STAGE_SIZE)
            
            # Enviar por UDP
            sender.send_position(*position)
            print(f"📍 Posición enviada: X={position[0]:.2f}, Y={position[1]:.2f}")
            
            previous_scan = current_scan
            time.sleep(SCAN_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo sistema...")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        lidar.close()
        sender.close()
        print("✅ Sistema detenido correctamente")

if __name__ == "__main__":
    main()