import bpy
import socket
import time
import math
from math import radians

# Connessione al server del Dobot
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 65401))


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

    # Applica gli angoli di rotazione ai giunti corretti
    if joint_objects['Joint1'] in bpy.data.objects:
        bpy.data.objects[joint_objects['Joint1']].rotation_euler[2] = math.radians(angles[0])  # Asse Z per Joint1
    if joint_objects['Joint2'] in bpy.data.objects:
        bpy.data.objects[joint_objects['Joint2']].rotation_euler[1] = math.radians(
            angles[1] + 26.925539016723633)  # Asse Y per Joint2 vedi se meno o piu
    if joint_objects['Joint3'] in bpy.data.objects:
        bpy.data.objects[joint_objects['Joint3']].rotation_euler[1] = math.radians(
            angles[2] + 28.57915496826172)  # Asse Y per Joint3
    # Aggiorna la scena
    bpy.context.view_layer.update()


try:
    data = client_socket.recv(256)  # Ricevi i dati dal server (buffer di 256 byte)
    joint_angles = data.decode('utf-8').strip().split(',')
    update_joint_angles(joint_angles)
    print("hello")
    # time.sleep(2)
except KeyboardInterrupt:
    print("Shutdown requested by user")
finally:
    client_socket.close()
    print("Client shutdown")