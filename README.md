# Digital Twin del braccio robotico:Dobot Magician

## Prerequisiti

1. **Hardware**: Dobot Magician connesso al PC tramite USB.
2. **Software**:
   - [Blender](https://www.blender.org/download/) (versione 4.1.1 o successive).
   - Python 3.12.
   - [Dobot SDK](https://www.dobot-robots.com/service/download-center) installato per Python.

3. **Dipendenze Python**:
   - Seguire le istruzioni alla sezione ufficiale: __DobotDemoForPython64__

## Installazione

1. **Clonazione del Repository**

2. **Configurazione del Dobot**
- Scarica e installa il driver per il Dobot Magician.
- Assicurati che il Dobot sia acceso e connesso tramite USB.

3. **Configurazione di Blender**
- Apri Blender e carica il file `Blender/DobotMagician3D.blend`.

## Esecuzione del Progetto

Il progetto è composto da due parti principali: il lato Dobot (che comunica con il braccio fisico) e il lato Blender (che controlla il modello 3D). Segui questi passaggi in base alla direzione del collegamento che vuoi effettuare:

### Fisico-Virtuale: invia gli angoli dal Dobot Magician al modello 3D di Blender
- Avvia lo script 'DobotServerSocket.py'.
- Apri Blender e nella sezione Scripting avvia il file 'Blender/BlenderClientSocket.py'.
- Muovendo il braccio robotico in modalità manuale il modello 3D di Blender si muoverà nella nuova posizione del Dobot.

### Virtuale-Fisico: invia gli angoli dal modello 3D di Blender al Dobot Magician 
- Apri Blender e nella sezione Scripting avvia il file 'Blender/BlenderServerSocket.py'.
- Avvia lo script 'DobotClientSocket.py'.
- Muovendo il modello 3D su Blender, il Dobot si muoverà nella posizione del modello digitale.

## Altri script utili
### 'DobotGetJointAnglesFromAPI.py'
- Per ottenere gli angoli del Dobot Magician
### 'MoveDobotJointByAngles.py' 
- Inserisci gli angoli dei Joint1, Joint2, Joint3, Joint4 ed avviando lo script il Dobot Magician si sposterà nella posizione con gli angoli inseriti.
### 'TestAnglesForBlenderClientSocket.py'
- Apri Blender e nella sezione Scripting avvia il file 'Blender/BlenderServerSocket.py'.
- Avvia lo script per ottenere le angolazioni trasmesse da Blender.
### Sviluppi Futuri
I seguenti script rappresentano due nuove strategie per ottimizzare il collegamento del Digital Twin: una utilizza due script (uno lato fisico e uno lato digitale) che aprono due connessioni sockets per scambiarsi le angolazioni dei modelli e l'altra utilizza due script ma con una sola connessione socket in cui entrambi gli script si comportano sia da Server che da Client condividendo il buffer: inviando e ricevendo dati ad intervalli e con determinate condizioni.
- 'DobotComunicationTwoSockets.py' e 'DobotComunicationOneSocket.py' lato Dobot Magician.
- 'Blender/BlenderComunicationTwoSockets.py' e 'Blender/BlenderComunicationOneSocket.py' lato Blender.

# Documentazione Ufficiale Dobot
# DobotDemoForPython64

DobotDemoForPython64 is the demo of python package dynamic library files. It can be used directly by the python function to control Dobot Magician.

This document describes the secondary development environment building and demo python codes, frameworks, and systems, aiming to help secondary developer to understand common API of Dobot Magician and build development environment quickly.


## Files Description

- Dll files contain the api functions needed to control Dobot Magician.
- DobotDllType.py : Specific implementing file. This section encapsulate api functions provided by the dll as python function.
- DobotControl.py : Secondary encapsulation of Dobot API. In order to get you up and running quickly, the code in the example adds a certain comment for easy reading.Examples are as follows:

```python
#将dll读取到内存中并获取对应的CDLL实例
#Load Dll and get the CDLL object
api = dType.load()

#建立与dobot的连接
#Connect Dobot
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])
```

## Python API

DobotDllType.py encapsulates the C type interface of Dobot DLL, which is Python API of Dobot. The example for loading DLL is shown as follows.

```PYTHON
def load():
    if platform.system() == "Windows":
        return CDLL("DobotDll.dll",  RTLD_GLOBAL)
    elif platform.system() == "Darwin" :
        return CDLL("libDobotDll.dylib",  RTLD_GLOBAL)
    elif platform.system() == "Linux":
        return cdll.loadLibrary("libDobotDll.so")
```

## Usage

- For Windows OS, please add the DLLs directory to environment variable Path.
- For Linux OS, please add the following statement at the end of `~/.bash_profile` file and restart computer.
```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:DOBOT_LIB_PATH
```
- For Mac OS
If the following error occurs, the solution is:
```python
File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/ctypes/__init__.py", line 356, in __init__
    self._handle = _dlopen(self._name, mode)
OSError: dlopen(libDobotDll.dylib, 10): image not found
```

```
% cd DobotDemoForPython
% otool -L libDobotDll.dylib
```
The executable_path part, all use the tools of `install_name_tool` to modify the path.

```python
# install _name_tool -change <old path> <new path> libDobotDll.dylib
install_name_tool -change @executable_path/QtSerialPort.framework/Versions/5/QtSerialPort /Users/outannexway/Downloads/Dobot/DobotDemoV2.0-20170118/DobotDemoForPython/QtSerialPort.framework/Versions/5/QtSerialPort libDobotDll.dylib
```
- cd DobotDemoForPython
Use vscode debugging, be sure to use the DobotDemoForPython path
- Connect the Dobot Magician
- python DobotControl.py

## Attention

##### There are the following points to note:
- You need to add the DLL address to the system environment variable
- A 32-bit system corresponds to a 32-bit dynamic library, and a 64-bit system corresponds to a 64-bit dynamic library
- please use the python 64 bit environment.


