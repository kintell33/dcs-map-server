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
        data = (await loop.sock_recv(client, 2048))
        for wsclient in WSCLIENTS:
            try:
                if not data:
                    process = False
                else:
                    json = get_clean_json(data)
                    await wsclient.send(bytes(convert_list_to_string(add_entity_type(json)), 'utf-8'))
            except Exception as error:
                print(str(error))
                WSCLIENTS.remove(wsclient)
    client.close()

def convert_list_to_string(list):
    response = "["
    first = True
    for item in list:
        if first:
            response = response + json.dumps(item)
            first = False
        else:
            response = response + ',' + json.dumps(item)
    return response + ']'

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
    data = str(data).replace('b"[','[').replace("'", '"').replace("\n", " ").replace("]'", "]").replace("},]\"", "}]")
    data = json.loads(data)
    return data


def ws_clients_remove(wsclient):
    print("Remove {} from websocket clients".format(str(wsclient.id)))
    WSCLIENTS.remove(wsclient)


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
