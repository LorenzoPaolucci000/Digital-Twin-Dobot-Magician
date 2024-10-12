#import bpy     #TODO Togliere il commento quando si esegue su Blender
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


# Funzione per ottenere gli angoli di rotazione dei joint
def get_joint_angles_rotation(joint_objects):
    rotations = []

    for joint_name, object_name in joint_objects.items():
        obj = bpy.data.objects.get(object_name)
        if obj:
            if joint_name == 'Joint1':
                # Per PivotArm (asse Z)
                rotation_angle = math.degrees(obj.rotation_euler.z)
                rotations.append(rotation_angle)
            elif joint_name == 'Joint2' or joint_name == 'Joint3':
                # Per RearArm e ForeArm (asse Y)
                rotation_angle = math.degrees(obj.rotation_euler.y)
                rotations.append(rotation_angle)
    return rotations


# Funzione per configurare il server socket e inviare i dati
def start_server_socket(host='localhost', port=12388):
    def server_thread():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Server listening for connections {port}...")
        client_socket, client_address = server_socket.accept()
        print(f"Connected by {client_address}")

        try:
            while True:
                joint_rotations = get_joint_angles_rotation(joint_objects)
                if joint_rotations:
                    data_to_send = ','.join([f"{angle:.2f}" for angle in joint_rotations])+"$"
                    client_socket.sendall(data_to_send.encode())
                    print(f"Sent: {data_to_send}")
                time.sleep(0.5)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()
            server_socket.close()

    thread = threading.Thread(target=server_thread)
    thread.start()


# Avvia il server socket in modo non bloccante
bpy.app.timers.register(lambda: start_server_socket() or None, first_interval=1.0)
