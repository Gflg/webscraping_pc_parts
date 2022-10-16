import json
from pcpartpicker import API
api = API()

def write_to_file(item, data):
    with open(f'pcpartpicker-{item}.json', 'w') as file:
        json.dump(data, file)

parts = ["cpu", "motherboard", "video-card", "memory", "power-supply"]
all_data = []
for part in parts:
    data = api.retrieve(part).to_json()
    data = json.loads(data)[part]
    write_to_file(part, data)