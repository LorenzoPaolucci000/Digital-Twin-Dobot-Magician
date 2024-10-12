import DobotDllType as dType
import time

api = dType.load()
port = 'COM3'

# Connessione al Dobot Magician
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

# Funzione per impostare gli angoli dei Joint e ottenre l'indice del comando in coda
def set_joint_angles(j1, j2, j3, j4):
    # Usa SetPTPCmd con PTPMode.PTPMOVJANGLE per specificare gli angoli dei giunti
    queuedCmdIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJANGLEMode, j1, j2, j3, j4, 1)[0]
    pose = dType.GetPose(api)
    joint_angles = pose[4:7]  # Estrae gli angoli dei joint: 1, 2, 3
    print(f"Joint Angles: {joint_angles}")
    return queuedCmdIndex

try:
    # Esempio di angoli dei Joint
    joint_angles = [0, 0, 0, 0]  # Angoli in gradi per J1, J2, J3, J4

    # Imposta gli angoli dei Joint e ottieni l'indice del comando in coda
    cmd_index = set_joint_angles(joint_angles[0], joint_angles[1], joint_angles[2], joint_angles[3])

    # Avvia l'esecuzione dei comandi in coda
    dType.SetQueuedCmdStartExec(api)

    # Attendi che il movimento sia completato (l'indice del comando eseguito è lo stesso o ha superato l'indice del comdando richiesto)
    while True:
        currentIndex = dType.GetQueuedCmdCurrentIndex(api)[0]
        if currentIndex >= cmd_index:
            break
        time.sleep(0.1)

except KeyboardInterrupt:
    # Gestione dell'interruzione per liberare la porta COM
    print("Interruzione ricevuta, disconnessione in corso...")

finally:
    # Ferma l'esecuzione dei comandi in coda
    dType.SetQueuedCmdStopExec(api)
    # Assicurati che il Dobot sia sempre disconnesso alla fine
    dType.DisconnectDobot(api)
    print("Dobot disconnesso correttamente")
