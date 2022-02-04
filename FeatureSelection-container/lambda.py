import json
import pymongo
import boto3
import pandas as pd
from datetime import datetime
from getSchema import getSchema, existing_reduced_schema
from getEncodedData import getEncodedData, take_info_from_schema#, getModelVersions
from feature_selection import feature_selection
from ENV_definitions import ENV_db_client_URL,ENV_db_database,ENV_testFS_to_pipelineSNS

db_client = pymongo.MongoClient(ENV_db_client_URL)
db = db_client[ENV_db_database]

def lambda_handler(event, context): 
    print("FunctionFeatureSelection Received event: " + json.dumps(event, indent=2))
    message = event['Records'][0]['Sns']['Message']
    print("From SNS:: " + message)
    messageJSON = json.loads(message) 
    model_id = messageJSON['model'] # NLmodel_xx
    
    
    # objId = messageJSON['_id']
    #str_time_stamp = messageJSON['time_stamp'] ###
    owner = messageJSON['owner']
    featureSelection = messageJSON['featureSelection']
    # name_for_model,msg = encoder_column(ObjectId(objId),model_id,db) # name_for_model ==NLmodel_xx_for_model
    model_name = db[model_id].find_one()['modelname']
    
    print(owner)
    print(model_name)
    
    
    data_encoded = getEncodedData(owner, model_name, db) #all data received
    print('data',data_encoded)
    #print(type(data_encoded)) #dict type
    full_data_schema = getSchema(owner, model_name, db) #original schema
    print('original schema',full_data_schema)
    #print(type(full_data_schema))

    data_input = pd.json_normalize(data_encoded['record'])
    selected_features = feature_selection(data_input)
    print('selected_features',selected_features)    

    # 
    schema_input = full_data_schema['input']

    drop_list = []
    for i, feature in enumerate(schema_input):
        if feature['name'] not in selected_features:
            drop_list.append(feature['name'])
            del schema_input[i]

    if existing_reduced_schema(selected_features, owner, model_name, db):
        print('there exist a schema has same selected features list')
    else: 

        del full_data_schema['_id']
        full_data_schema.update({'fs' : 'processed'})

        for schema in db[model_id].find({'schema':'yes'}): #print existing schema
            print(schema)
        db[model_id].insert(full_data_schema) #insert new schema
    model_id_for_model = model_id+'_for_model'
    sns = boto3.client('sns')
    response = sns.publish ( #specify role of ec2 to use sns.publish
        TopicArn = ENV_testFS_to_pipelineSNS,
            
        Message = '{"model":"' + model_id_for_model + '","featureSelection":"' + featureSelection + '","owner":"' + owner + '"}'
    )
    print('response:',response)	
    db[model_id].find_one_and_update({'features':'yes'},{'$set':{'features':'yes','drop_features':drop_list,'selected_features':selected_features}},upsert=True)
    db[model_id].update({ "process_check":"yes"},{"$set":{"status":"Finish encoding and feature selection"}})
    print('Finish feature selection')
    return message
