'''def getModelVersions(owner,model,db):
    
    #import time
    #start = time.time()
    
    docs = db["customer_model_table"].find({'owner':owner})
    for doc in docs:
        models = (doc["models"])
    print('get')
    for model_item in models:
        if model_item['model_name']== model:
            schema_is_in = (model_item['ID'])
    model_id_for_model = schema_is_in+'_for_model'
    docs = db[model_id_for_model].find({"model_version": "yes"})
    print(model_id_for_model)
    print(docs)
    for doc in docs:
        model_version = doc
        
        #end = time.time()
        #print("getModelVersions time:"+str(end-start))
        print(versions)
        return model_version, model_id_for_model'''

def take_info_from_schema(name, type_, db):
    
    #import time
    #start = time.time()
    
    data_type = 0
    schema = db[name].find({ "schema":"yes" })
    if (type_.lower() =="numerical"):
        data_col = []
        data_type =1
    elif (type_.lower() =="categorical"):
        data_col = {}
        addition_info = "max_categories"
        data_type =1
    elif (type_.lower() =="ordinal"):
        data_col = {}
        addition_info = "ordinality"
        data_type =1
    elif(type_.lower() =="text"):
        data_col = {}
        addition_info = "text_schema"
        data_type =1
    elif (type_.lower() =="ner_input"):
        data_col = []
        data_type =1
    elif (type_.lower() =="ner_output"):
        data_col = []
        data_type =1
    elif (type_.lower() =="ner_output"):
        data_col = []
        data_type =1
    elif (type_.lower() =="sa_input"):
        data_col = {}
        addition_info = "max_sentence_length"
        data_type =1
    elif (type_.lower() =="recommendation_input"):
        data_col = {}
        addition_info = "recommendation_schema"
        data_type =1


    elif (type_.lower() == 'input'):
        data_col = []
        data_type =2
    elif (type_.lower() == 'output'):
        data_col = []
        data_type =2
    elif (type_.lower()=='all'):
        data_type = 3
    else:
        return "invalid type"


    if (data_type ==1):
        for schema_doc in schema:
            input_data = schema_doc['input']
            for i in range(len(input_data)):
                if (input_data[i]['type'].lower()== type_.lower()):
                    if (input_data[i]['type'] in ["numerical","ner_input","ner_output"]):
                        data_col.append(input_data[i]['name'])
                    else:
                        data_col[input_data[i]['name']] = input_data[i][addition_info]
    elif (data_type ==2):
        for schema_doc in schema:
            data = schema_doc[type_]
            for i in range(len(data)):
                data_col.append(data[i]['name'])
    
    #end = time.time()
    #print("take_info_from_schema time:"+str(end-start))
    
    return data_col

def getEncodedData(owner,model,db):
    
    import time
    start = time.time()
    
    docs = db["customer_model_table"].find({'owner':owner})
    for doc in docs:
        models = (doc["models"])
    
    for model_item in models:
        if model_item['model_name']== model:
            schema_is_in = (model_item['ID'])    
    
    
    docs = db[schema_is_in+"_for_model"].find( { "schema":"no" })#.limit(2)
    #docs  =  db[schema_is_in+"_for_model"].find({"schema":"no"})
    #docs  =  db[schema_is_in+"_for_model"].find({"schema":"no"}) .skip(db[schema_is_in+"_for_model"].count() - 400)
    temp = []
    categorical_col = []
          
    numerical_col = take_info_from_schema(schema_is_in,"numerical", db)
    output_col = take_info_from_schema(schema_is_in, "output",db)
    ordinal_dict = take_info_from_schema(schema_is_in, "ordinal",db)
    ordinal_col = list(ordinal_dict.keys())
    
    categorical_dict = take_info_from_schema(schema_is_in, "categorical",db)
    categorical_col = list(categorical_dict.keys())
    
    text_dict = take_info_from_schema(schema_is_in, "text",db)
    text_col = list(text_dict.keys())
    
    ner_input_col = take_info_from_schema(schema_is_in, "ner_input",db)
    ner_output_col = take_info_from_schema(schema_is_in, "ner_output",db)

    sa_input_dict = take_info_from_schema(schema_is_in, "sa_input",db)
    sa_input_col = list(sa_input_dict.keys())
    

    all_col =ordinal_col +numerical_col+ categorical_col + output_col + text_col + ner_input_col + ner_output_col + sa_input_col
#*******************************************************
#    all_col.append("note")

    for doc in docs:
        try:
            for key in list(doc.keys()):
                if key not in all_col: 
                    del doc[key]
                ###############
#                if key in ordinal_col or key in numerical_col:
#                    if pd.isnull(doc[key]):
#                        doc[key]=0
#                elif key in categorical_col:
#                    if pd.isnull(doc[key]):
#                        doc[key]=0
        except KeyError:
            pass

        temp.append(doc)
        
    
    temp_dict = {"owner":owner,"record":temp}
    
    end = time.time()
    print("getEncodedData time:"+str(end-start))
    
    return temp_dict