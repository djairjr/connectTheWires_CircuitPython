# Connect the Wires - CircuitPython Version
import board, busio, time, random, digitalio
import neopixel, adafruit_pcf8575
import adafruit_fancyled.adafruit_fancyled as fancy
import pwmio
# Criei esse arquivo com todas as cores já convertidas
from htmlColorCodes import CRGB 

global activeCon
global signal
global connections
global connectionName
global names
global numConnections
global numPlugs
global lastState

# Usando o i2c padrão da placa, com board.SDA e board.SCL
i2c = board.I2C()

# Criando o objeto plug, no endereço i2c padrão do módulo
plug = adafruit_pcf8575.PCF8575(i2c, 0x20)

# Atribuindo o número de canais e de conexões do jogo
numPlugs  = 16
numConnections = 4
random.seed(numPlugs)

#Desligando o Neopixel da placa para usar Ring externo
power = digitalio.DigitalInOut(board.NEOPIXEL_POWER)
power.switch_to_output(value=False)

#Criando a gauge luminosa em Neopixel
numLeds = 24 # Neopixel Ring
gauge = neopixel.NeoPixel(board.NEOPIXEL, numLeds, brightness=0.2)

# Utilizar um VU analógico
vuMeter = pwmio.PWMOut(board.A1)

# Claro, a fechadura magnética de sempre
magLock = digitalio.DigitalInOut (board.D2)
magLock.direction = digitalio.Direction.OUTPUT
magLock.value = True

signal = []
pannelDict = {}
connectionName = [[],[]]
names = ["Pin_" + str(i) for i in range (numPlugs)]

for plugPin in range (numPlugs): 
    signal.append (plug.get_pin(plugPin))
    signal[plugPin].switch_to_input(pull=digitalio.Pull.UP)
    pannelDict[signal[plugPin]]= names[plugPin]

connections = [
        [ signal[0], signal[1] ],
        [ signal[2], signal[3] ],
        [ signal[4], signal[5] ],
        [ signal[6], signal[7] ],
        [ signal[8], signal[9] ],
        [ signal[10], signal[11] ],
        [ signal[12], signal[13] ],
        [ signal[14], signal[15] ],     
        ]

# This list is just for print adequate solution when debugging
connectionName = [
     [pannelDict[signal[0]],  pannelDict[signal[1]]],
     [pannelDict[signal[2]],  pannelDict[signal[3]]],
     [pannelDict[signal[4]],  pannelDict[signal[5]]],
     [pannelDict[signal[6]],  pannelDict[signal[7]]],
     [pannelDict[signal[8]],  pannelDict[signal[9]]],
     [pannelDict[signal[10]],  pannelDict[signal[11]]],
     [pannelDict[signal[12]],  pannelDict[signal[13]]],
     [pannelDict[signal[14]],  pannelDict[signal[15]]],
    ]

lastState = [ False for i in range (numConnections)]
  
def isConnected (outputPin, inputPin):
    outputPin.switch_to_output (value=False)
    inputPin.switch_to_input(pull=digitalio.Pull.UP)
    return not (inputPin.value)

def randomConnections():    
    print ("Embaralhando Conexões")

    # get a random pair of signal   
    for i in range (len (signal)):
        j = random.randrange(0, i+1)       
        temp = signal[i]        
        signal[i] = signal[j]
        signal[j] = temp
    
    # This list is just for print adequate solution when debugging
    connectionName = [
         [pannelDict[signal[0]],  pannelDict[signal[1]]],
         [pannelDict[signal[2]],  pannelDict[signal[3]]],
         [pannelDict[signal[4]],  pannelDict[signal[5]]],
         [pannelDict[signal[6]],  pannelDict[signal[7]]],
         [pannelDict[signal[8]],  pannelDict[signal[9]]],
         [pannelDict[signal[10]],  pannelDict[signal[11]]],
         [pannelDict[signal[12]],  pannelDict[signal[13]]],
         [pannelDict[signal[14]],  pannelDict[signal[15]]],
        ]
    
    connections = [
        [ signal[0], signal[1] ],
        [ signal[2], signal[3] ],
        [ signal[4], signal[5] ],
        [ signal[6], signal[7] ],
        [ signal[8], signal[9] ],
        [ signal[10], signal[11] ],
        [ signal[12], signal[13] ],
        [ signal[14], signal[15] ],     
        ]
    
           
def updateGauge (num):
    gaugeStart = 2
    gaugeEnd = 12
    
    if num < 0:
        num = 0
        
    if num > 4:
        num = 4

    colorbar = [
        [CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Red'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'] ],
        [CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Red'], CRGB['OrangeRed'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'] ],
        [CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Red'], CRGB['OrangeRed'], CRGB['Orange'], CRGB['Orange'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'] ],
        [CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Red'], CRGB['OrangeRed'], CRGB['Orange'], CRGB['Orange'], CRGB['Yellow'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'] ],
        [CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Red'], CRGB['OrangeRed'], CRGB['Orange'], CRGB['Orange'], CRGB['Yellow'], CRGB['YellowGreen'], CRGB['Green'], CRGB['Green'], CRGB['Green'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'], CRGB['Black'] ]
      ]
    
    for i in range (gaugeStart):
        gauge [i] = CRGB['Black']
        gauge.show()
    
    for i in range (gaugeStart, gaugeEnd):
        gauge[i] = colorbar[num][i]
        gauge.show()
    
    for i in range (gaugeEnd, numLeds):
        gauge [i] = CRGB['Black']
        gauge.show()
        
randomConnections()

while (True) :
    # The Game Loop Start Here
    activeCon = 0
    allWiresCorrect = True
    stateChanged = False
    
    for i in range (numConnections):
        currentState = isConnected (connections[i][0], connections[i][1])
        if currentState != lastState[i]:
            stateChanged = True
            lastState[i] = currentState
        
        if currentState == True :
            activeCon = activeCon + 1
        else:
            allWiresCorrect = False
        
        vuMeterLevel = activeCon * 16384 #max level is 65535
        
        if vuMeterLevel > 65535 :
            vuMeterLevel = 65535
        
        vuMeter.duty_cycle = vuMeterLevel
        updateGauge (activeCon)
        
        if stateChanged :
            for i in range (len (connectionName)):
                print (connectionName[i][0], " connected to ", connectionName[i][1] )
        
        if all (lastState):
            magLock.value = False
            print ("Puzzle Solved")
        else:
            activeCon = 0
            magLock.value = True
            print ("Puzzle Unsolved")
        
        
