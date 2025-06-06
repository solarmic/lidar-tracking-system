import socket

class UDPSender:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"📡 UDP configurado para {host}:{port}")
    
    def send_position(self, x, y):
        """Envía posición normalizada por UDP"""
        try:
            message = f"{x:.4f},{y:.4f}"
            self.sock.sendto(message.encode(), (self.host, self.port))
        except Exception as e:
            print(f"⚠️ Error enviando UDP: {str(e)}")
    
    def close(self):
        self.sock.close()
        print("📡 Conexión UDP cerrada")
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()