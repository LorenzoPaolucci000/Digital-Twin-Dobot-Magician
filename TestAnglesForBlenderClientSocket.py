import socket
import time

# Connessione al server del Dobot
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 65001))


def update_joint_angles(angles):
    """
    Aggiorna gli angoli dei giunti del modello 3D in Blender.
    Angles è una lista contenente gli angoli in gradi.
    """
    # Nomi degli oggetti in Blender
    joint_objects = {
        'Joint1': 'PivotArm',
        'Joint2': 'RearArm',
        'Joint3': 'ForeArm',
    }

    # Convertire gli angoli in gradi a radianti per Blender
    angles = [float(angle) for angle in angles]
    print(angles)
    # Applica gli angoli di rotazione ai giunti corretti



try:
    while True:
        data = client_socket.recv(256)  # Ricevi i dati dal server
        if not data:
            break
        joint_angles = data.decode('utf-8').strip().split(',')
        print(f"Server Joint angles: {joint_angles}")
        update_joint_angles(joint_angles)
        time.sleep(0.1)
        # Aggiorna la scena
        # bpy.context.view_layer.update()
except KeyboardInterrupt:
    print("Shutdown requested by user")
finally:
    client_socket.close()
    print("Client shutdown")
