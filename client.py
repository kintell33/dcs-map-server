import socket
import asyncio

HOST = '127.0.0.1'
PORT = 9595


async def send_data():
    print('STARTING')
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    count = 0
    while count != 1:
        message = "[{'name':'SA9M38M1','group':'No Group','coalition':'Enemies','latitude':'42.07427932257','longitude':'43.064359500867','altitude':'2940.0658739824'},]"
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
