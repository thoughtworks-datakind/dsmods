import pandas as pd
from tableschema import Table
from dateutil.parser import parse

def is_date(string):
    if str(string) == "":
        return True
    try: 
        parse(string)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

def infer(path, limit = 2000):
    table = Table(path)
    table.infer(limit=limit, confidence=0.75)

    data = pd.read_csv(path, low_memory=False)
    num_rows = data.index._stop
    
    rows_to_scan = limit if limit < num_rows else num_rows

    metadata_array = []
    for field in table.schema.fields: 
        metadata = Metadata()
        
        metadata.name = field.name
        metadata.type = field.type 
        metadata.format = field.format

        object_description = data[field.name].astype(object).describe()
        
        missing_count = num_rows - int(object_description['count'])
        metadata.missing_count = missing_count
        metadata.missing_percentage =  round(float(missing_count)/num_rows  * 100 , 2)

        distinct_count = int(object_description['unique'])
        metadata.distinct_count = distinct_count
        metadata.distinct_percentage = round(float(distinct_count) / (num_rows - missing_count) * 100, 2)
        
        metadata.most_frequent = object_description['top']

        if metadata.type == "string" and metadata.missing_percentage != 100.0:
            if rows_to_scan == data[field.name].head(rows_to_scan).apply(lambda x :is_date(x)).sum():
                metadata.type = "date"
        
        if metadata.type ==  "integer" or metadata.type == "number" :
            numeric_description = data[field.name].describe()
            metadata.min = numeric_description['min']
            metadata.max = numeric_description['max']
        
        metadata_array.append(metadata)

    return metadata_array

class Metadata:

    name = ""
    type = ""
    format = ""
    missing_count = 0
    missing_percentage = 0.0
    distinct_count = 0
    distinct_percentage = 0.0
    most_frequent = object()
    min = 0.0
    max = 0.0