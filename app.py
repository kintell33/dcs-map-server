import asyncio
import socket
import websockets
import json

SOCKET_HOST = '127.0.0.1'
SOCKET_PORT = 9595
WEBSOCKET_HOST = 'localhost'
WEBSOCKET_PORT = 8765
WSCLIENTS = []
PROPERTY_TYPE = 'type'


class EntityDcsTypes:
    PLANE = 'plane'
    MISILE = 'misile'
    ALLIES = 'allies'
    ENEMIES = 'enemies'
    UNKNOWN = '-'


async def start_socket():
    print('STARTING SOCKET SERVER ON ' + str(SOCKET_PORT))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SOCKET_HOST, SOCKET_PORT))
    server.listen()
    server.setblocking(False)
    loop = asyncio.get_event_loop()
    while True:
        client, _ = await loop.sock_accept(server)
        loop.create_task(handle_client(client))


async def handle_client(client):
    loop = asyncio.get_event_loop()
    process = True
    while process:
        # read the message length header
        header = await loop.sock_recv(client, 4)
        if not header:
            process = False
            break
        msg_len = int.from_bytes(header, byteorder='big')

        # read the message based on the length in the header
        data = b''
        while len(data) < msg_len:
            packet = await loop.sock_recv(client, min(msg_len - len(data), 2048))
            if not packet:
                process = False
                break
            data += packet
        
        # process the message
        if process:
            json_data = get_clean_json(data)
            
            if json_data:
                entity_data = add_entity_type(json_data)
                for wsclient in WSCLIENTS:
                    try:
                        await wsclient.send(bytes(convert_list_to_string(entity_data), 'utf-8'))
                    except Exception as error:
                        print(str(error))
                        WSCLIENTS.remove(wsclient)

    client.close()


def convert_list_to_string(data):
    return json.dumps(data)


def add_entity_type(entity_dcs):

    for item in entity_dcs:
        if 'Player' in item.get('group'):
            item[PROPERTY_TYPE] = EntityDcsTypes.PLANE
        elif item.get('group') == 'No Group':
            item[PROPERTY_TYPE] = EntityDcsTypes.MISILE
        elif item.get('coalition') == 'Allies':
            item[PROPERTY_TYPE] = EntityDcsTypes.ALLIES
        elif item.get('coalition') == 'Enemies':
            item[PROPERTY_TYPE] = EntityDcsTypes.ENEMIES
        else:
            item[PROPERTY_TYPE] = EntityDcsTypes.UNKNOWN

    return entity_dcs


def get_clean_json(data):
    try:
        print(str(data))
        data = data.decode('utf-8')
        print(str(data))
        data = data.replace('b"[','[').replace('\n', ' ').replace('[,', '[').replace(",]", "]").replace("'",'"')
        print(str(data))
        data = json.loads(data)
        print('to return data:'+str(data))
        return data
    except Exception as error:
        print(error)
        return ""


async def start_websocket():
    print('STARTING WEBSOCKET ON ' + str(WEBSOCKET_PORT))
    async with websockets.serve(on_web_socket_message, WEBSOCKET_HOST, WEBSOCKET_PORT):
        await asyncio.Future()


async def on_web_socket_message(websocket, path):
    print(str(path))
    async for message in websocket:
        if message == 'listen':
            WSCLIENTS.append(websocket)
            print('Connected ' + str(websocket.id))
            await websocket.send('accepted')


print('STARTING...')
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(start_socket(), start_websocket()))
