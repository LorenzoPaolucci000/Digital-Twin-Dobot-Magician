import DobotDllType as dType
import socket
import time

# Connessione al Dobot Magician
api = dType.load()
port = 'COM3'
CON_STR = {
    dType.DobotConnect.DobotConnect_NoError: "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"
}
state = dType.ConnectDobot(api, port, 115200)[0]
if state != dType.DobotConnect.DobotConnect_NoError:
    print("Failed to connect Dobot:", CON_STR[state])
    exit()

# Setup Server Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 65004))
server_socket.listen(1)
print("Server listening for connections...")
client_socket, addr = server_socket.accept()
print('Connected by', addr)

# Setup Client Socket to change
# client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket1.connect(('localhost', 65035))
# client_socket1.setblocking(False)

# Funzione per ottenere gli angoli dei joint
def get_joint_angles(): 
    pose = dType.GetPose(api)
    joint_angles = pose[4:7]  # Estrae gli angoli dei joint: 1, 2, 3
    print(f"Joint Angles: {joint_angles}")
    return joint_angles


try:
    while True:
        angles = get_joint_angles()
        data = ','.join(map(str, angles)) + '\n'  # formatta gli angoli con la virgola
        client_socket.sendall(data.encode('utf-8'))
        # client socket test
        #data1 = client_socket1.recv(128)
        #print(data1.decode('utf-8'))
        time.sleep(0.5)  # update rate
except KeyboardInterrupt:
    print("Shutdown requested by user")
except BlockingIOError:
    # Se non ci sono dati disponibili
    pass
finally:
    client_socket.close()
    server_socket.close()
    dType.DisconnectDobot(api)
    print("Server shutdown, Dobot disconnected")
