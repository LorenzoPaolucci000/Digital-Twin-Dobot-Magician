import DobotDllType as dType
import time

# Carica la libreria Dobot
api = dType.load()

# Porta USB del pc
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

# Funzione per ottenere la posizione corrente
def get_current_pose():
    pose = dType.GetPose(api)
    return pose


# Funzione per ottenere gli angoli dei joint
def get_joint_angles():
    pose = dType.GetPose(api)
    # Estrae gli angoli dei joint: 1, 2, 3
    joint_angles = pose[4:7]  # extracting joint angles
    print(f"Joint Angles: {joint_angles}")  # Print to verify axes
    return joint_angles


try:
    # Loop per ottenere i dati in tempo reale
    while True:
        angles = get_joint_angles()
        print("Current JointAngles:", angles)
        pose = get_current_pose()
        print("Current Pose:", pose)
        time.sleep(1)
except KeyboardInterrupt:
    # Gestione dell'interruzione per liberare la porta COM
    print("Shutdown requested by user")
finally:
    # Assicurati che il Dobot sia sempre disconnesso alla fine
    dType.DisconnectDobot(api)
    print("Dobot disconnected successfully")
