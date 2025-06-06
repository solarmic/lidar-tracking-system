import numpy as np

class PositionTracker:
    def __init__(self):
        self.last_valid_position = (0.5, 0.5)  # Posición central por defecto
        self.movement_threshold = 0.05  # 5% del escenario
        self.static_counter = 0
        
    def polar_to_cartesian(self, angle, distance):
        """Convierte coordenadas polares a cartesianas (relativas al centro)"""
        rad = np.radians(angle)
        x = distance * np.sin(rad)
        y = distance * np.cos(rad)
        return x, y
        
    def normalize_position(self, x, y, stage_size):
        """Normaliza coordenadas a rango [0,1]"""
        norm_x = 0.5 + (x / (stage_size * 1000))  # stage_size en metros, distance en mm
        norm_y = 0.5 + (y / (stage_size * 1000))
        return max(0, min(1, norm_x)), max(0, min(1, norm_y))
    
    def detect_main_target(self, scan_data, stage_size):
        """Detecta el objetivo principal (persona) en los datos del LIDAR"""
        if not scan_data:
            self.static_counter += 1
            if self.static_counter > 10:
                print("⚠️ No se detectan objetivos. Usando última posición válida")
            return self.last_valid_position
            
        # Agrupar puntos cercanos
        clusters = []
        for angle, dist in scan_data:
            x, y = self.polar_to_cartesian(angle, dist)
            added = False
            for cluster in clusters:
                c_x, c_y, c_count = cluster
                distance = np.sqrt((x - c_x)**2 + (y - c_y)**2)
                if distance < 500:  # 50cm de radio
                    cluster[0] = (c_x * c_count + x) / (c_count + 1)
                    cluster[1] = (c_y * c_count + y) / (c_count + 1)
                    cluster[2] += 1
                    added = True
                    break
            if not added:
                clusters.append([x, y, 1])
        
        # Seleccionar el cluster más grande (persona)
        if clusters:
            main_cluster = max(clusters, key=lambda c: c[2])
            x, y, count = main_cluster
            new_position = self.normalize_position(x, y, stage_size)
            
            # Detectar movimiento significativo
            movement = np.sqrt((new_position[0] - self.last_valid_position[0])**2 + 
                             (new_position[1] - self.last_valid_position[1])**2)
            
            if movement > self.movement_threshold:
                self.last_valid_position = new_position
                self.static_counter = 0
                print(f"👤 Persona detectada (puntos: {count})")
            else:
                self.static_counter += 1
                if self.static_counter > 5:
                    print("⏸️ Persona estática. Usando última posición")
                
        return self.last_valid_position