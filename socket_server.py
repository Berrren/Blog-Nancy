import socket
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, MoveTank
from time import sleep

# Configuración de los motores
motor_left = LargeMotor(OUTPUT_B)  # Motor izquierdo en el puerto B
motor_right = LargeMotor(OUTPUT_C)  # Motor derecho en el puerto C
tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)

# Configuración de la conexión del servidor
HOST = '0.0.0.0'  # Acepta conexiones desde cualquier dirección
PORT = 8000        # Puerto en el que se espera la conexión (asegúrate de usar el mismo puerto en Unity)

# Creación del socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print("Esperando conexión...")

# Aceptar la conexión
client_socket, addr = server_socket.accept()
print("Conectado a " + str(addr))  # Cambio aquí

try:
    # Escuchar y recibir datos continuamente
    while True:
        data = client_socket.recv(1024)  # Recibe hasta 1024 bytes de datos
        if not data:
            break
        
        data = data.decode('utf-8')  # Decodifica los datos recibidos como string
        print(f"Datos recibidos: {data}")

        # Movimientos según el comando recibido
        if data == 'move_forward':
            print("Moviendo hacia adelante")
            tank_drive.on(50, 50)  # Mueve ambos motores hacia adelante con una velocidad de 50
        elif data == 'move_backward':
            print("Moviendo hacia atrás")
            tank_drive.on(-50, -50)  # Mueve ambos motores hacia atrás con una velocidad de -50
        elif data == 'turn_left':
            print("Girando a la izquierda")
            tank_drive.on(-50, 50)  # Motor izquierdo hacia atrás y derecho hacia adelante (giro)
        elif data == 'turn_right':
            print("Girando a la derecha")
            tank_drive.on(50, -50)  # Motor izquierdo hacia adelante y derecho hacia atrás (giro)
        elif data == 'stop':
            print("Deteniendo el robot")
            tank_drive.off()  # Detiene los motores
        else:
            print("Comando desconocido")
    
    # Cerrar la conexión después de terminar
    client_socket.close()

except KeyboardInterrupt:
    print("Interrumpido, cerrando el servidor")
    client_socket.close()
