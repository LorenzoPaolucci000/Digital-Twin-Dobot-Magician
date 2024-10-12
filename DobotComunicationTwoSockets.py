import socket
import DobotDllType as dType
import time
import threading


# Connessione al Dobot Magician
def connect_dobot(port='COM3'):
    api = dType.load()
    CON_STR = {
        dType.DobotConnect.DobotConnect_NoError: "DobotConnect_NoError",
        dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
        dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"
    }
    state = dType.ConnectDobot(api, port, 115200)[0]
    if state == dType.DobotConnect.DobotConnect_NoError:
        print("Dobot connected successfully")
    else:
        print("Failed to connect Dobot:", CON_STR[state])
        exit()
    return api


# Funzione per impostare gli angoli dei Joint e ottenere l'indice del comando in coda
def set_joint_angles(api, j1, j2, j3, j4):
    # j2 e j3 negativi perché su blender hanno segno opposto
    queuedCmdIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJANGLEMode, j1, -j2, -j3, j4, 1)[0]
    return queuedCmdIndex


# Attende che il movimento sia completato
def wait_for_movement(api, cmd_index):
    while dType.GetQueuedCmdCurrentIndex(api)[0] < cmd_index:
        time.sleep(0.1)


# Funzione per ottenere gli angoli attuali dei joint
def get_joint_angles(api):
    pose = dType.GetPose(api)
    joint_angles = pose[4:7]  # Estrae gli angoli dei joint: 1, 2, 3
    formatted_angles = [f"{angle:.2f}" for angle in joint_angles]
    print(f"Dobot Joint Angles: {formatted_angles}")
    return joint_angles


# Funzione server per inviare gli angoli del Dobot a Blender
def server_socket_thread(api):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 65004))
    server_socket.listen(1)
    print("Server listening for connections...")
    client_socket, addr = server_socket.accept()
    print('Connected by', addr)

    try:
        while True:
            angles = get_joint_angles(api)
            data = ','.join([f"{angle:.2f}" for angle in angles]) + '\n'
            client_socket.sendall(data.encode('utf-8'))
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutdown requested by user")
    finally:
        client_socket.close()
        server_socket.close()

# Funzione client per ricevere gli angoli da Blender e trasmetterli al Dobot
def client_socket_thread(api, host='localhost', port=12307):
    # Avvia l'esecuzione dei comandi in coda
    dType.SetQueuedCmdStartExec(api)

    # Tentativi di connessione fino a quando il server Blender non è attivo
    connected = False
    while not connected:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            connected = True
            print(f"Connected to {host}:{port}")
        except ConnectionRefusedError:
            print("Waiting for Blender server to start...")
            time.sleep(1)
        finally:
            if not connected:
                client_socket.close()

    try:
        while True:
            data = client_socket.recv(512).decode()
            if not data:
                break
            data = data.split("$")          # Per evitare di concatenare più valori in un array
            angles = data[0].split(',')
            print(f"Angles Joint: {angles}")
            joint_angles = [float(angle) for angle in angles]
            cmd_index = set_joint_angles(api, joint_angles[0], joint_angles[1], joint_angles[2], 0)
            wait_for_movement(api, cmd_index)
    except KeyboardInterrupt:
        print("Shutdown requested by user")
    finally:
        dType.SetQueuedCmdStopExec(api)
        dType.DisconnectDobot(api)
        client_socket.close()
        print("Client shutdown, Dobot disconnected")



# Funzione principale per avviare entrambi i thread
def main():
    api = connect_dobot()

    # Avviare il thread per il server socket
    server_thread = threading.Thread(target=server_socket_thread, args=(api,))
    server_thread.start()

    # Avviare il thread per il client socket
    client_thread = threading.Thread(target=client_socket_thread, args=(api,))
    client_thread.start()

    # Aspetta che entrambi i thread terminino
    server_thread.join()
    client_thread.join()


if __name__ == "__main__":
    main()
