from tableschema import Table

def infer(path, limit = 2000):
    table = Table(path)
    table.infer(limit=limit, confidence=0.75)
    return table.schema