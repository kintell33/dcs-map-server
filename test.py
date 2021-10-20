import json

misile_data = "b\"[{'name':'SA9M38M1','group':'No Group','coalition':'Enemies','latitude':'42.07427932257','longitude':'43.064359500867','altitude':'2940.0658739824'},]\""

def clean_data(data):
    data = str(data).replace("'",'"').replace("\n", " ").replace("]'", "]").replace("},]", "}]")
    json_message = json.loads(data)
    return json.dumps(json_message)

def get_clean_json(data):
    data = str(data).replace('b"[','[').replace("'", '"').replace("\n", " ").replace("]'", "]").replace("},]\"", "}]")
    print(data)
    object = json.loads(data)
    return add_entity_type(object)

def add_entity_type(entity_dcs):
    for item in entity_dcs:
        if item.get('group') == 'No Group':
            item['type'] = 'misile'
    
    return entity_dcs

print(get_clean_json(misile_data))