import bpy
import socket
import threading
import time
import math

# Nomi dei Joint in Blender
joint_objects = {
    'Joint1': 'PivotArm',
    'Joint2': 'RearArm',
    'Joint3': 'ForeArm',
}

# Flag globale per interrompere il thread
running = True

# Funzione per ottenere gli angoli attuali del modello 3D in Blender
def get_joint_angles_rotation(joint_objects):
    rotations = []

    for joint_name, object_name in joint_objects.items():
        obj = bpy.data.objects.get(object_name)
        if obj:
            # Controllo del giunto specifico per determinare l'asse corretto
            if joint_name == 'Joint1':
                # Rotazione sull'asse Z per Joint1
                rotation_angle = round(math.degrees(obj.rotation_euler.z), 2)
                rotations.append(rotation_angle)
            elif joint_name == 'Joint2' or joint_name == 'Joint3':
                # Rotazione sull'asse Y per Joint2 e Joint3
                rotation_angle = round(math.degrees(obj.rotation_euler.y), 2)
                rotations.append(rotation_angle)

    print(f"Blender Joint Angles: {rotations}")
    return rotations

# Funzione per aggiornare il modello 3D di Blender con i nuovi angoli ricevuti
def update_joint_angles(angles):
    for joint_name, object_name in joint_objects.items():
        obj = bpy.data.objects.get(object_name)
        if obj:
            # Aggiornamento dell'angolo di rotazione del giunto specifico
            if joint_name == 'Joint1':
                # Imposta la rotazione sull'asse Z per Joint1
                obj.rotation_euler.z = math.radians(angles[0])
            elif joint_name == 'Joint2':
                # Imposta la rotazione sull'asse Y per Joint2
                obj.rotation_euler.y = math.radians(-angles[1])
            elif joint_name == 'Joint3':
                # Imposta la rotazione sull'asse Y per Joint3
                obj.rotation_euler.y = math.radians(-angles[2])

    print(f"Updated Blender Model with angles: {angles}")

# Funzione per configurare il server socket e gestire i dati
def start_server_socket(host='localhost', port=65000):
    def server_thread():
        global running
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Server waiting for connection on port {port}...")
        client_socket, addr = server_socket.accept()
        print(f"Connected to {addr}")

        try:
            while running:
                # Ricevi gli angoli del Dobot
                data = client_socket.recv(512).decode()
                if data.startswith("DOBOT"):
                    angles = list(map(float, data.split(':')[1].split(',')))
                    bpy.app.timers.register(lambda: update_joint_angles(angles) or None)

                # Invia gli angoli di Blender al Dobot
                angles = get_joint_angles_rotation(joint_objects)
                client_socket.sendall(f"ANGLES:{','.join(map(str, angles))}".encode('utf-8'))
                time.sleep(0.5)
        except Exception as e:
            print(f"Error in server socket: {e}")
        finally:
            client_socket.close()
            server_socket.close()
            print("Server socket closed")

    # Avvia il thread del server
    thread = threading.Thread(target=server_thread)
    thread.start()

    # Funzione di pulizia quando si interrompe il timer
    def stop_thread():
        global running
        running = False
        print("Server thread stopping")
        return None

    # Avvia il timer per il cleanup
    bpy.app.timers.register(stop_thread, first_interval=1.0)

# Avvia il server socket in modo non bloccante
bpy.app.timers.register(lambda: start_server_socket() or None, first_interval=1.0)
