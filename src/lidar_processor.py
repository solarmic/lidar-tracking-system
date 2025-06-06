import numpy as np
from rplidar import RPLidar

class LidarProcessor:
    def __init__(self, port):
        self.port = port
        self.lidar = None
        self.connect()
        self.STAGE_SIZE = 6  # 6x6 metros
        self.MIN_DISTANCE = 300  # 30cm (en mm)
        self.MAX_DISTANCE = 4000  # 4m (en mm)
        self.reset_scan()
        
    def connect(self):
        """Establece conexión con el LIDAR"""
        try:
            self.lidar = RPLidar(self.port)
            print(f"🔌 LIDAR conectado en {self.port}")
        except Exception as e:
            raise ConnectionError(f"No se pudo conectar al LIDAR en {self.port}: {str(e)}")
        
    def reset_scan(self):
        self.scan_data = []
        
    def capture_scan(self):
        """Captura un escaneo completo del LIDAR"""
        self.reset_scan()
        try:
            for scan in self.lidar.iter_scans():
                for (_, angle, distance) in scan:
                    if self.MIN_DISTANCE < distance < self.MAX_DISTANCE:
                        self.scan_data.append((angle, distance))
                break
            return self.scan_data
        except Exception as e:
            # Reconectar si hay error
            print(f"⚠️ Error en captura: {str(e)}. Reintentando conexión...")
            self.close()
            self.connect()
            return self.capture_scan()
    
    def filter_moving_targets(self, current_scan, previous_scan, movement_threshold=100):
        """Filtra objetivos en movimiento comparando con escaneo anterior"""
        if not previous_scan or not current_scan:
            return current_scan
            
        moving_points = []
        for (angle, dist) in current_scan:
            # Encontrar punto más cercano en el escaneo anterior
            closest = min(previous_scan, key=lambda p: abs(p[0] - angle))
            if abs(dist - closest[1]) > movement_threshold:
                moving_points.append((angle, dist))
                
        return moving_points if moving_points else current_scan
    
    def close(self):
        if self.lidar:
            try:
                self.lidar.stop()
                self.lidar.disconnect()
                print("🔌 LIDAR desconectado")
            except:
                pass
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()