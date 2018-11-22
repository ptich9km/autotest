#!/usr/bin/python

import serial, time

# initialization and open the port
# possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call
ser = serial.Serial()
ser.port = "/dev/ttyUSB1"
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
ser.parity = serial.PARITY_NONE  # set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE  # number of stop bits
# ser.timeout = None          #block read
ser.timeout = 1  # non-block read
# ser.timeout = 2              #timeout block read
ser.xonxoff = False  # disable software flow control
ser.rtscts = False  # disable hardware (RTS/CTS) flow control
ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control
ser.writeTimeout = 2  # timeout for write


# Connect to board using serial port with speed 'baudrate'
def connect_to_board(baudrate):
    try:
        ser.baudrate = baudrate
        if (ser.isOpen() == False):
            ser.open()
        ser.flushInput()  # flush input buffer, discarding all its contents
        ser.flushOutput()  # flush output buffer, aborting current output
        return True
    except Exception as e:
        print("Error open serial port: " + str(e))
        return False

# Connect to board with number of try
def try_connect_to_board(baudrate, count_of_Try):
    tryCount = count_of_Try
    connection = connect_to_board(baudrate)
    while tryCount > 0 and connection == False:
        connection = connect_to_board(baudrate)
        tryCount = tryCount - 1
        time.sleep(1)
    if tryCount == 0 and connection == False:
        print("Critical error in opening serial port")
        exit()

# Close serial port
def Close_serial_board():
    try:
        ser.close()
        return True
    except Exception as e:
        print("Error open serial port: " + str(e))
        return False

# Set reset in line
def try_Set_line_in_reset():
    try:
        Resetbyte = (b'\xf0')
        tryCount = 4
        lineState = 0
        ser.write(Resetbyte)
        time.sleep(0.5)  # give the serial port sometime to receive the data
        response = ser.readline()
        while response == b'\xf0' or response == b'' and tryCount != 0:
            ser.write(Resetbyte)
            time.sleep(0.5)
            response = ser.readline()
            tryCount = tryCount - 1
            print('Try reset line state - {}' + str(tryCount))
        if response != b'\xf0' or b'':
            print('Device detected - {} '.format(response))
            lineState = 1
    except Exception as e:
        print("There is a problem in reseting line state: " + str(e))
    return lineState

# Send 1 bit information, 1 or 0
def SendBit(bit):
    try:
        if bit == 0:
            Zerobyte = (b'\x00')
            ser.write(Zerobyte)
            #time.sleep(0.5)
            cheakBit = ser.read(1)
            if cheakBit != b'\x00':
                print("Readed 0 bit not the same")
        elif bit == 1:
            Onebyte = (b'\xff')
            ser.write(Onebyte)
            #time.sleep(0.5)
            cheakBit = ser.read(1)
            if cheakBit != b'\xff':
                print("Readed 1 bit not the same")
        else:
            print("Sended bit is not correct")
    except Exception as e:
        print("Error in sending bit : " + str(e))
        exit()

# Send 1 byte of information
def SendByte(byte):
    try:
        sendByte = []
        for i in range(8):
            bit = byte & 0x01;
            SendBit(bit)
            sendByte.append(bit)
            time.sleep(0.1)
            byte = byte >> 1
    except Exception as e:
        print("error open serial port: " + str(e))
        exit()

#Read 1 bit information, FF or 0
def ReadBit():
    try:
        Zerobyte = (b'\xff')
        ser.write(Zerobyte)
        time.sleep(0.1)
        cheakBit = ser.read(1)
        if cheakBit == b'\xff':
            return 1
        else:
            return 0
    except Exception as e:
        print("error open serial port: " + str(e))
        exit()

# Read 1 byte information
def ReadByte():
    byte = []
    for i in range(8):
        #print("Operation number is {}".format(i))
        bit = ReadBit()
        #time.sleep(0.1)
        byte.append(bit)
    #print(byte)
    byte.reverse()
    byte = ''.join(map(str, byte))
    #print(byte)
    byte = int(byte, 2)
    #print(byte)
    byte = hex(byte)
    return byte

# Calculate CRC8 from data array
def Count_CRC8(dataArray):
    crc = 0x00
    for data in dataArray:
        for i in range(8):
            temp = (crc ^ data) & 0x1
            if (temp == 1):
                crc = (crc) ^ 0x18

            crc = (crc >> 1) & 0x7f

            if(temp == 1):
                crc |= 0x80

            data >>= 1
    return crc

ON_RELAY = 0x39  # Включить реле питания и/или балансира на аккумуляторе
OFF_RELAY = 0x3A  # Выключить реле питания и/или балансира на аккумуляторе
REQ_UUID = 0x30  # Запрос UUID
REQ_UID = 0x31  # Запрос UserID
SETUP_UID = 0x32  # Установка UserID
CLEAR_UID = 0x33  # Очистка UserID (обезличивание)
REQ_SERIAL = 0x34  # Запрос SerialNumber
SAVE_LOG = 0x35  # Сохранить один лог
RESTORE_LOG = 0x36  # Считать один лог
REQ_CAPACITY = 0x37  # Запрос значения ёмкости аккумулятора
SETUP_CAPACITY = 0x38  # Установка значения ёмкости аккумулятора
REQ_PARAM = 0x3B  # Запрос параметров аккумулятора (напряжение, температура, ток)
STX = 0xAA #Инициализация линии

def Linda(type_operation, operation):

    if type_operation == 'send':
        data = []
        time.sleep(0.3)
        if operation == ON_RELAY:
            data.append(STX)
            data.append(ON_RELAY)
            data.append(0x02)
            data.append(0x01)
            data.append(0x01)
            crc8_from_Data = Count_CRC8(data)
            data.append(crc8_from_Data)
            lineState = try_Set_line_in_reset()
            print("ON_RELAY sended to device {}".format(data))
            if lineState == 1:
                time.sleep(0.3)
                try_connect_to_board(115200, 5)
                SendByte(0xcc)
                time.sleep(0.1)
                for i in data:
                    SendByte(i)
                    time.sleep(0.1)
            else:
                print("Any devices not detected")

        elif operation == OFF_RELAY:
            data.append(STX)
            data.append(OFF_RELAY)
            data.append(0x02)
            data.append(0x01)
            data.append(0x01)
            crc8_from_Data = Count_CRC8(data)
            data.append(crc8_from_Data)
            lineState = try_Set_line_in_reset()
            print("OFF_RELAY sended to device {}".format(data))
            if lineState == 1:
                time.sleep(0.3)
                try_connect_to_board(115200, 5)
                SendByte(0xcc)
                time.sleep(0.1)
                for i in data:
                    SendByte(i)
                    time.sleep(0.1)
                time.sleep(0.3)
            else:
                print("Any devices not detected")

        elif operation == REQ_CAPACITY:
            data.append(STX)
            data.append(REQ_CAPACITY)
            data.append(0x0)
            crc8_from_Data = Count_CRC8(data)
            data.append(crc8_from_Data)
            lineState = try_Set_line_in_reset()
            print("REQ_CAPACITY sended to device {}".format(data))
            if lineState == 1:
                time.sleep(0.3)
                try_connect_to_board(115200, 5)
                SendByte(0xcc)
                time.sleep(0.1)
                for i in data:
                    SendByte(i)
                    time.sleep(0.1)
                time.sleep(0.3)
            else:
                print("Any devices not detected")

        elif operation == SETUP_CAPACITY:
            data.append(STX)
            data.append(SETUP_CAPACITY)
            data.append(0x05)
            data.append(0x10)
            data.append(0x0)
            data.append(0x0)
            data.append(0x0)
            data.append(0x0)
            crc8_from_Data = Count_CRC8(data)
            data.append(crc8_from_Data)
            lineState = try_Set_line_in_reset()
            print("SETUP_CAPACITY sended to device {}".format(data))
            if lineState == 1:
                time.sleep(0.3)
                try_connect_to_board(115200, 5)
                SendByte(0xcc)
                time.sleep(0.1)
                for i in data:
                    SendByte(i)
                    time.sleep(0.1)
                time.sleep(0.3)
            else:
                print("Any devices not detected")

        elif operation == RESTORE_LOG:
            data.append(STX)
            data.append(RESTORE_LOG)
            data.append(0x0)
            crc8_from_Data = Count_CRC8(data)
            data.append(crc8_from_Data)
            lineState = try_Set_line_in_reset()
            print("RESTORE_LOG sended to device {}".format(data))
            if lineState == 1:
                time.sleep(0.3)
                try_connect_to_board(115200, 5)
                SendByte(0xcc)
                time.sleep(0.1)
                for i in data:
                    SendByte(i)
                    time.sleep(0.1)
                time.sleep(0.3)
            else:
                print("Any devices not detected")

        elif operation == SAVE_LOG:
            data.append(STX)
            data.append(SAVE_LOG)
            data.append(0x2d)

            data.append(0x0)
            data.append(0x18)
            data.append(0x13)
            data.append(0x8)
            data.append(0x3)
            data.append(0x10)
            data.append(0x25)
            data.append(0x13)
            data.append(0x0)
            data.append(0x0)
            data.append(0x0)
            data.append(0x0)
            data.append(0x0)
            data.append(0x0)
            data.append(0x0)
            data.append(0x0)
            data.append(0x0)
            data.append(0x0)
            data.append(0x0)
            data.append(0x0)
            data.append(0x0)
            data.append(0x0)
            data.append(0x0)
            data.append(0x0)
            data.append(0x0)
            data.append(0x0)
            data.append(0xa)
            data.append(0x1a)
            data.append(0xcd)
            data.append(0xcc)
            data.append(0xcc)
            data.append(0x40)
            data.append(0x0)
            data.append(0x0)
            data.append(0x60)
            data.append(0x40)
            data.append(0x25)
            data.append(0x28)
            data.append(0xb8)
            data.append(0xb)
            data.append(0x0)
            data.append(0x0)
            data.append(0x4d)
            data.append(0x0)
            data.append(0x0)
            crc8_from_Data = Count_CRC8(data)
            data.append(crc8_from_Data)
            lineState = try_Set_line_in_reset()
            print("SAVE_LOG sended to device {}".format(data))
            if lineState == 1:
                time.sleep(0.3)
                try_connect_to_board(115200, 5)
                SendByte(0xcc)
                time.sleep(0.1)
                for i in data:
                    SendByte(i)
                    time.sleep(0.1)
                time.sleep(0.3)
            else:
                print("Any devices not detected")

        elif operation == REQ_SERIAL:
            data.append(STX)
            data.append(REQ_SERIAL)
            data.append(0x0)
            crc8_from_Data = Count_CRC8(data)
            data.append(crc8_from_Data)
            lineState = try_Set_line_in_reset()
            print("REQ_SERIAL sended to device {}".format(data))
            if lineState == 1:
                time.sleep(0.3)
                try_connect_to_board(115200, 5)
                SendByte(0xcc)
                time.sleep(0.1)
                for i in data:
                    SendByte(i)
                    time.sleep(0.1)
                time.sleep(0.3)
            else:
                print("Any devices not detected")

        elif operation == CLEAR_UID:
            data.append(STX)
            data.append(CLEAR_UID)
            data.append(0x0)
            crc8_from_Data = Count_CRC8(data)
            data.append(crc8_from_Data)
            lineState = try_Set_line_in_reset()
            print("CLEAR_UID sended to device {}".format(data))
            if lineState == 1:
                time.sleep(0.3)
                try_connect_to_board(115200, 5)
                SendByte(0xcc)
                time.sleep(0.1)
                for i in data:
                    SendByte(i)
                    time.sleep(0.1)
                time.sleep(0.3)
            else:
                print("Any devices not detected")

        elif operation == REQ_UID:
            data.append(STX)
            data.append(REQ_UID)
            data.append(0x0)
            crc8_from_Data = Count_CRC8(data)
            data.append(crc8_from_Data)
            lineState = try_Set_line_in_reset()
            print("REQ_UID sended to device {}".format(data))
            if lineState == 1:
                time.sleep(0.3)
                try_connect_to_board(115200, 5)
                SendByte(0xcc)
                time.sleep(0.1)
                for i in data:
                    SendByte(i)
                    time.sleep(0.1)
                time.sleep(0.3)
            else:
                print("Any devices not detected")

        elif operation == SETUP_UID:
            data.append(STX)
            data.append(SETUP_UID)
            data.append(0x8)
            data.append(0x1)
            data.append(0x0)
            data.append(0x0)
            data.append(0x0)
            data.append(0x1)
            data.append(0x0)
            data.append(0x0)
            data.append(0x0)
            crc8_from_Data = Count_CRC8(data)
            data.append(crc8_from_Data)
            lineState = try_Set_line_in_reset()
            print("SETUP_UID sended to device {}".format(data))
            if lineState == 1:
                time.sleep(0.3)
                try_connect_to_board(115200, 5)
                SendByte(0xcc)
                time.sleep(0.1)
                for i in data:
                    SendByte(i)
                    time.sleep(0.1)
                time.sleep(0.3)
            else:
                print("Any devices not detected")

        elif operation == REQ_UUID:
            data.append(STX)
            data.append(REQ_UUID)
            data.append(0x0)
            crc8_from_Data = Count_CRC8(data)
            data.append(crc8_from_Data)
            lineState = try_Set_line_in_reset()
            print("REQ_UUID sended to device {}".format(data))
            if lineState == 1:
                time.sleep(0.3)
                try_connect_to_board(115200, 5)
                SendByte(0xcc)
                time.sleep(0.1)
                for i in data:
                    SendByte(i)
                    time.sleep(0.1)
                time.sleep(0.3)
            else:
                print("Any devices not detected")

        else:
            print("{} - Sended operation not correct".format(operation))

    elif type_operation == 'read':
        time.sleep(0.3)
        readData1 = []
        if operation == ON_RELAY:
            for i in range(4):
                readData1.append(ReadByte())
        if operation == OFF_RELAY:
            for i in range(4):
                readData1.append(ReadByte())
        if operation == REQ_CAPACITY:
            for i in range(9):
                readData1.append(ReadByte())
        if operation == SETUP_CAPACITY:
            for i in range(4):
                readData1.append(ReadByte())
        if operation == RESTORE_LOG:
            for i in range(45):
                readData1.append(ReadByte())
        if operation == SAVE_LOG:
            for i in range(4):
                readData1.append(ReadByte())
        if operation == REQ_SERIAL:
            for i in range(9):
                readData1.append(ReadByte())
        if operation == CLEAR_UID:
            for i in range(4):
                readData1.append(ReadByte())
        if operation == SETUP_UID:
            for i in range(4):
                readData1.append(ReadByte())
        if operation == REQ_UID:
            for i in range(11):
                readData1.append(ReadByte())
        if operation == REQ_UUID:
            for i in range(20):
                readData1.append(ReadByte())
        print("Readed data from device {}".format(readData1))
        time.sleep(1)
        return readData1

    else:
        print("{} - Type operation not correct".format(type_operation))


import re

# Send 1 command is serial port and receive data array
def sendCmd(input):
    try:
        ser.write(input.encode())
        time.sleep(0.1)
        dataArray = []
        data = ser.readline()
        startSendingdata_time = time.clock()
        print("Sending data in serial port: {}".format(input))
        # cheaktimer if data isn't going for 3 sec
        if len(data) == 0:
            lostData_time = time.clock()
        while len(data) == 0 and (lostData_time - startSendingdata_time) < 3:
            time.sleep(1)
            lostData_time = time.clock()
            print("There isn't any data, system is waiting")
        while not len(data) == 0:
            data = ser.readline()
            # cheak if data has spases and non-data information
            if data != b'# \r\n' and data != b'# ' and data != b'':
                data = (data[0:-2])
                data = data.decode('ascii')
                dataWithout_non_printable_characters = re.sub(r'(\x1b[/[])[0-9]?[;]?[0-9]?[0-9]{1}m', "", data)
                dataArray.append(dataWithout_non_printable_characters)
    except Exception as e:
        print("Can't send data in serial port: " + str(e))
        exit()
    return dataArray

