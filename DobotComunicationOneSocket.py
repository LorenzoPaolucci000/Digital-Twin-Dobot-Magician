import socket
import DobotDllType as dType
import time
import threading

#TODO: Da verificare e migliorare

# Connessione al Dobot Magician
def connect_dobot(port='COM3'):
    api = dType.load()
    state = dType.ConnectDobot(api, port, 115200)[0]
    if state != dType.DobotConnect.DobotConnect_NoError:
        print("Failed to connect Dobot")
        exit()
    return api

# Funzione per ottenere gli angoli dei joint
def get_joint_angles(api):
    pose = dType.GetPose(api)
    joint_angles = [round(angle, 2) for angle in pose[4:7]]  # Angoli con 2 decimali
    print(f"Dobot Joint Angles: {joint_angles}")
    return joint_angles

# Funzione per impostare gli angoli dei joint
def set_joint_angles(api, angles):
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJANGLEMode, *angles, 1)

# Funzione server-client condivisa
def server_client_thread(api, host='localhost', port=65000):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to {host}:{port}")

    try:
        while True:
            # Attendere per ricevere dati da Blender
            data = client_socket.recv(512).decode()
            if data.startswith("ANGLES"):
                # Ricevi gli angoli da Blender e aggiorna Dobot
                angles = list(map(float, data.split(':')[1].split(',')))
                set_joint_angles(api, angles)
                print(f"Set Joint Angles to: {angles}")

            # Invia gli angoli del Dobot a Blender
            angles = get_joint_angles(api)
            client_socket.sendall(f"DOBOT:{','.join(map(str, angles))}".encode('utf-8'))
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Shutdown requested")
    finally:
        client_socket.close()

def main():
    api = connect_dobot()
    server_client_thread(api)

if __name__ == "__main__":
    main()
