import socket
import asyncio

HOST = '127.0.0.1'
PORT = 9595

TEST_MESSAGE = [
    {
        "name": "SA9M38M1",
        "group": "No Group",
        "coalition": "Enemies",
        "latitude": "42.07427932257",
        "longitude": "43.064359500867",
        "altitude": "2940.0658739824"
    },
    {
        "name": "SU25T",
        "group": "No Group",
        "coalition": "Allies",
        "latitude": "41.240300",
        "longitude": "48.005150",
        "altitude": "5000.000000"
    },
    {
        "name": "F-15C",
        "group": "Player",
        "coalition": "Allies",
        "latitude": "39.960000",
        "longitude": "32.819000",
        "altitude": "20000.000000"
    },
    {
        "name": "F-14B",
        "group": "No Group",
        "coalition": "Allies",
        "latitude": "37.470000",
        "longitude": "-122.000000",
        "altitude": "15000.000000"
    },
    {
        "name": "SU-27",
        "group": "No Group",
        "coalition": "Enemies",
        "latitude": "40.500000",
        "longitude": "30.000000",
        "altitude": "12000.000000"
    },
    {
        "name": "AH-64D",
        "group": "Player",
        "coalition": "Allies",
        "latitude": "36.115000",
        "longitude": "-115.212000",
        "altitude": "5000.000000"
    },
    {
        "name": "SA342M",
        "group": "No Group",
        "coalition": "Allies",
        "latitude": "45.245000",
        "longitude": "37.714000",
        "altitude": "1000.000000"
    },
    {
        "name": "AV-8BNA",
        "group": "Player",
        "coalition": "Allies",
        "latitude": "37.934000",
        "longitude": "-75.466000",
        "altitude": "15000.000000"
    },
    {
        "name": "A-10C",
        "group": "No Group",
        "coalition": "Allies",
        "latitude": "42.200000",
        "longitude": "-76.100000",
        "altitude": "8000.000000"
    },
    {
        "name": "KA-50",
        "group": "No Group",
        "coalition": "Enemies",
        "latitude": "46.373000",
        "longitude": "30.219000",
        "altitude": "3000.000000"
    },
    {
        "name": "F-16C",
        "group": "No Group",
        "coalition": "Allies",
        "latitude": "36.888400",
        "longitude": "-107.437000",
        "altitude": "10000.000000"
    },
    {
        "name": "Mig-29S",
        "group": "No Group",
        "coalition": "Enemies",
        "latitude": "38.881400",
        "longitude": "121.695000",
        "altitude": "9000.000000"
    },
    {
        "name": "SA9M38M1",
        "group": "No Group",
        "coalition": "Enemies",
        "latitude": "42.07427932257",
        "longitude": "43.064359500867",
        "altitude": "2940.0658739824"
    },
    {
        "name": "SU25T",
        "group": "No Group",
        "coalition": "Allies",
        "latitude": "41.240300",
        "longitude": "48.005150",
        "altitude": "5000.000000"
    },
    {
        "name": "F-15C",
        "group": "Player",
        "coalition": "Allies",
        "latitude": "39.960000",
        "longitude": "32.819000",
        "altitude": "20000.000000"
    },
    {
        "name": "F-14B",
        "group": "No Group",
        "coalition": "Allies",
        "latitude": "37.470000",
        "longitude": "-122.000000",
        "altitude": "15000.000000"
    },
    {
        "name": "SU-27",
        "group": "No Group",
        "coalition": "Enemies",
        "latitude": "40.500000",
        "longitude": "30.000000",
        "altitude": "12000.000000"
    },
    {
        "name": "AH-64D",
        "group": "Player",
        "coalition": "Allies",
        "latitude": "36.115000",
        "longitude": "-115.212000",
        "altitude": "5000.000000"
    },
    {
        "name": "SA342M",
        "group": "No Group",
        "coalition": "Allies",
        "latitude": "45.245000",
        "longitude": "37.714000",
        "altitude": "1000.000000"
    },
    {
        "name": "AV-8BNA",
        "group": "Player",
        "coalition": "Allies",
        "latitude": "37.934000",
        "longitude": "-75.466000",
        "altitude": "15000.000000"
    },
    {
        "name": "A-10C",
        "group": "No Group",
        "coalition": "Allies",
        "latitude": "40.200000",
        "longitude": "-76.100000",
        "altitude": "8000.000000"
    },
    {
        "name": "KA-50",
        "group": "No Group",
        "coalition": "Enemies",
        "latitude": "46.373000",
        "longitude": "30.219000",
        "altitude": "3000.000000"
    }
]


async def send_data():
    print('STARTING')
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    count = 0
    while count != 1:
        message = str(TEST_MESSAGE)
        print('MESSAGE SEND')
        message_bytes = bytes(message, 'utf-8')
        # prepend the length of the message to the message itself
        length = len(message_bytes).to_bytes(4, byteorder='big')
        message_to_send = length + message_bytes
        print('sending '+str(message_to_send))
        client.send(message_to_send)
        count = count + 1
        await asyncio.sleep(1)
    client.close()
    print('CLOSING')

asyncio.run(send_data())
