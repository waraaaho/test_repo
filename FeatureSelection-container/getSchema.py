

def getSchema(owner, model, db):
    
    #import time
    #start = time.time()
    
    docs = db["customer_model_table"].find({'owner':owner})
    for doc in docs:
        models = (doc["models"])
    
    for model_item in models:
        if model_item['model_name']== model:
            schema_is_in = (model_item['ID'])
        
    docs = db[schema_is_in].find({"owner":owner, "schema":"yes" })
    for doc in docs:
        schema = doc
        
        #end = time.time()
        #print("getSchema time:"+str(end-start))
        
        return schema #return first(original) schema

def existing_reduced_schema(selected_features, owner, model, db):
    docs = db["customer_model_table"].find({'owner':owner})
    for doc in docs:
        models = (doc["models"])
    
    for model_item in models:
        if model_item['model_name']== model:
            schema_is_in = (model_item['ID'])
        
    docs = db[schema_is_in].find({"owner":owner, "schema":"yes"})
    if docs.count()==1: return False #first time

    for doc in docs:  
        schema = doc
    print('found latest schema',schema)
    features = []
    for feature in schema['input']:
        features.append(feature['name'])
    features.sort()
    selected_features.sort()
    if features==selected_features:
        db[schema_is_in].update({ "fs": "processed"},{"$set":{'fs': 'continue'}}) #coninue training on one schema
        return True  
    db[schema_is_in].update({ "fs": "continue"},{"$set":{'fs': 'processed'}}) #as different schema revert old schema to processed state
    return False