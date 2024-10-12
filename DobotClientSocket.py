import socket
import DobotDllType as dType
import time


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


# Funzione che attende che il movimento sia completato
def wait_for_movement(api, cmd_index):
    while True:
        currentIndex = dType.GetQueuedCmdCurrentIndex(api)[0]
        if currentIndex >= cmd_index:
            break
        time.sleep(0.01)


# Funzione principale per il client socket
def start_client_socket(host='localhost', port=12388):
    api = connect_dobot()
    # Avvia l'esecuzione dei comandi in coda
    dType.SetQueuedCmdStartExec(api)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print(f"Connected to {host}:{port}")

        try:
            while True:
                data = client_socket.recv(512).decode()
                if not data:
                    break
                data = data.split("$")          # Per evitare di concatenare più valori in un array
                angles = data[0].split(',')
                print(f"Angles Joint: {angles}")
                joint_angles = [float(angle) for angle in angles]
                cmd_index = set_joint_angles(api, joint_angles[0], joint_angles[1], joint_angles[2],
                                             0)         # 0 per joint4 (da definire in base all'end-effector)
                wait_for_movement(api, cmd_index)

        except KeyboardInterrupt:
            print("Shutdown requested by user")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Ferma l'esecuzione dei comandi in coda
            dType.SetQueuedCmdStopExec(api)
            dType.DisconnectDobot(api)
            client_socket.close()
            print("Client shutdown, Dobot disconnected")


start_client_socket()


