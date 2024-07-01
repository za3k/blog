import yaml

def loads(s):
    parts = s.split("---\n", 2)
    assert len(parts) == 3
    assert parts[0] == ""
    front = yaml.safe_load(parts[1])
    front["content"] = parts[2]
    return front
def load(path):
    try: 
        with open(path) as f:
            return loads(f.read())
    except:
        print(path)
        raise
