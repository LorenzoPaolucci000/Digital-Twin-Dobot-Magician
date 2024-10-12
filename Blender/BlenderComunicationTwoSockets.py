import bpy
import socket
import threading
import math
import time

#TODO: Da imlementare meglio per evitare che Blender vada in deadlock

# Nomi dei Joint in Blender
joint_objects = {
    'Joint1': 'PivotArm',
    'Joint2': 'RearArm',
    'Joint3': 'ForeArm',
}

# Flag globale per la sincronizzazione
is_moving = False

# Funzione per ottenere gli angoli di rotazione dei joint dal modello 3D
def get_joint_angles_rotation(joint_objects):
    rotations = []
    for joint_name, object_name in joint_objects.items():
        obj = bpy.data.objects.get(object_name)
        if obj:
            if joint_name == 'Joint1':
                rotation_angle = math.degrees(obj.rotation_euler.z)
                rotations.append(rotation_angle)
            elif joint_name == 'Joint2' or joint_name == 'Joint3':
                rotation_angle = math.degrees(obj.rotation_euler.y)
                rotations.append(rotation_angle)
    return rotations

# Funzione per impostare gli angoli di rotazione sui joint del modello 3D
def set_joint_angles_rotation(joint_objects, angles):
    for joint_name, angle in zip(joint_objects.keys(), angles):
        obj = bpy.data.objects.get(joint_objects[joint_name])
        if obj:
            if joint_name == 'Joint1':
                obj.rotation_euler.z = math.radians(angle)
            elif joint_name == 'Joint2' or joint_name == 'Joint3':
                obj.rotation_euler.y = math.radians(angle)

# Funzione per gestire il server socket che riceve gli angoli dal Dobot
def server_socket_thread(host='localhost', port=65005):
    global is_moving
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}...")

    client_socket, addr = server_socket.accept()
    print('Connected by', addr)

    try:
        while True:
            data = client_socket.recv(512).decode().strip()
            if not data:
                break
            angles = [float(angle) for angle in data.split(',')]
            if not is_moving:
                set_joint_angles_rotation(joint_objects, angles)
    except Exception as e:
        print(f"Error in server socket: {e}")
    finally:
        client_socket.close()
        server_socket.close()

# Funzione per gestire il client socket che invia gli angoli del modello 3D al Dobot
def client_socket_thread(host='localhost', port=12306):
    global is_moving
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((host, port))
                print(f"Connected to {host}:{port}")

                while True:
                    angles = get_joint_angles_rotation(joint_objects)
                    data_to_send = ','.join([f"{angle:.2f}" for angle in angles])
                    client_socket.sendall(data_to_send.encode('utf-8'))
                    time.sleep(0.5)  # Frequenza di aggiornamento
        except ConnectionRefusedError:
            print("Waiting for Dobot server to start...")
            time.sleep(1)

# Funzione principale per avviare entrambi i thread (server e client) in Blender
def main():
    # Avviare il thread per il server socket (riceve angoli dal Dobot)
    server_thread = threading.Thread(target=server_socket_thread)
    server_thread.daemon = True
    server_thread.start()

    # Avviare il thread per il client socket (invia angoli al Dobot)
    client_thread = threading.Thread(target=client_socket_thread)
    client_thread.daemon = True
    client_thread.start()

    return 0.1  # Continua a chiamare il timer a intervalli di 0.1 secondi

if __name__ == "__main__":
    bpy.app.timers.register(main, first_interval=1.0)
