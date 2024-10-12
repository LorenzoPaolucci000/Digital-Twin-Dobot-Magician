import bpy
import socket
import math
from math import radians

# Connessione al server del Dobot
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 65004))
buffer_size = 256

# Nomi dei Joint in Blender
joint_objects = {
    'Joint1': 'PivotArm',
    'Joint2': 'RearArm',
    'Joint3': 'ForeArm',
}


def update_joint_angles():
    try:
        data = client_socket.recv(buffer_size)  # Riceve i dati dal server
        if data:
            joint_angles = data.decode('utf-8').strip().split(',')
            angles = [float(angle) for angle in joint_angles]

            # Applica gli angoli di rotazione ai Joint corretti
            if joint_objects['Joint1'] in bpy.data.objects:
                bpy.data.objects[joint_objects['Joint1']].rotation_euler[2] = math.radians(angles[0])  # Asse Z per Joint1
            if joint_objects['Joint2'] in bpy.data.objects:
                bpy.data.objects[joint_objects['Joint2']].rotation_euler[1] = math.radians(-angles[1]) # Asse Y per Joint2
            if joint_objects['Joint3'] in bpy.data.objects:
                bpy.data.objects[joint_objects['Joint3']].rotation_euler[1] = math.radians(-angles[2])  # Asse Y per Joint3

    except BlockingIOError:
        # Se non ci sono dati disponibili
        pass

    except Exception as e:
        print(f"Errore durante la ricezione dei dati: {e}")

    # Richiama questa funzione dopo un certo intervallo
    bpy.app.timers.register(update_joint_angles, first_interval=0.1)


# Imposta il socket in modalità non bloccante
client_socket.setblocking(False)

# Avvia il timer richiamando la funzione per aggiornare gli angoli
bpy.app.timers.register(update_joint_angles)
