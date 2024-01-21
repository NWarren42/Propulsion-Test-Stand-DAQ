import requests
from yamcs.client import YamcsClient

# Setting up a server using the HTTP API?

# Start the Yamcs server
requests.post('http://127.0.0.1:8090/api/services', json={
    'class': 'org.yamcs.http.HttpServer',
    'args': {
        'port': 8090,
        'webSocket': {
            'writeBufferWaterMark': {
                'low': 32768,
                'high': 65536
            }
        },
        'cors': {
            'allowOrigin': '*',
            'allowCredentials': False
        }
    }
})

# Create a session
session = requests.Session()
session.headers.update({'Content-Type': 'application/json'})

# Create a new instance
response = session.post('http://127.0.0.1:8090/api/instances', json={
    'name': 'my_instance',
    'description': 'My Yamcs instance'
})

# Get the instance ID
instance_id = response.json()['id']

# Create a new processor
response = session.post(f'http://127.0.0.1:8090/api/processors/{instance_id}', json={
    'name': 'my_processor',
    'description': 'My Yamcs processor'
})

# Get the processor ID
processor_id = response.json()['id']

# Create a new parameter
response = session.post(f'http://127.0.0.1:8090/api/parameters/{instance_id}/{processor_id}', json={
    'name': 'my_parameter',
    'description': 'My Yamcs parameter',
    'type': 'INT',
    'unit': 'm/s^2'
})

# Get the parameter ID
parameter_id = response.json()['id']

# Create a new command
response = session.post(f'http://127.0.0.1:8090/api/commands/{instance_id}/{processor_id}', json={
    'name': 'my_command',
    'description': 'My Yamcs command',
    'arguments': [
        {
            'name': 'arg1',
            'description': 'Argument 1',
            'type': 'INT',
            'unit': 'm/s^2'
        }
    ]
})

# Get the command ID
command_id = response.json()['id']



# Setting up the computer as a client using the Yamcs Python API
client = YamcsClient('localhost:8090')
mdb = client.get_mdb(instance = 'simulator')
archive = client.get_archive(instance = 'simulator')
processor = client.get_processor(instance = 'simulator', processor = 'realtime')

