import socket
import time
import math
from math import radians

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

# import bpy
# import socket
# import math
# from math import radians
#
# # Connessione al server del Dobot
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect(('localhost', 65432))
#
# # Buffer per ricevere i dati dal server
# buffer_size = 256
#
# # Nomi degli oggetti in Blender
# joint_objects = {
#     'Joint1': 'PivotArm',  # esempio di nome per Joint1, asse Z
#     'Joint2': 'RearArm',  # esempio di nome per Joint2, asse Y
#     'Joint3': 'ForeArm',  # esempio di nome per Joint3, asse Y
# }
#
#
# def update_joint_angles():
#     try:
#         data = client_socket.recv(buffer_size)  # Ricevi i dati dal server (buffer di 256 byte)
#         if data:
#             joint_angles = data.decode('utf-8').strip().split(',')
#             angles = [radians(float(angle)) for angle in joint_angles]
#
#             # Applica gli angoli di rotazione ai giunti corretti
#             if joint_objects['Joint1'] in bpy.data.objects:
#                 bpy.data.objects[joint_objects['Joint1']].rotation_euler[2] = math.radians(angles[0])  # Asse Z per Joint1
#             if joint_objects['Joint2'] in bpy.data.objects:
#                 bpy.data.objects[joint_objects['Joint2']].rotation_euler[1] = math.radians(-(angles[1] - 26.925539016723633)) # Asse Y per Joint2
#             if joint_objects['Joint3'] in bpy.data.objects:
#                 bpy.data.objects[joint_objects['Joint3']].rotation_euler[1] = math.radians(-(angles[2] - 28.57915496826172))  # Asse Y per Joint3
#
#     except BlockingIOError:
#         # Non ci sono dati disponibili, passiamo al prossimo ciclo
#         pass
#
#     except Exception as e:
#         print(f"Errore durante la ricezione dei dati: {e}")
#
#     # Richiama questa funzione dopo 0.1 secondi
#     bpy.app.timers.register(update_joint_angles, first_interval=0.1)
#
#
# # Imposta il socket in modalità non bloccante
# client_socket.setblocking(False)
#
# # Avvia il timer per aggiornare gli angoli dei giunti
# bpy.app.timers.register(update_joint_angles)
