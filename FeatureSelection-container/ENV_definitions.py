#  Environment settings
#


##  The below section is for DEVELOPMENT (DEV) environment only
##  
"""
ENV_environment = "DEV"            

ENV_db_client_URL = "mongodb://automl_user:secretPassword@ec2-54-82-39-90.compute-1.amazonaws.com/datalake"
ENV_db_database = 'datalake'

ENV_region='ap-southeast-1'

ENV_access_key_id='AKIASVMYAA2LBYBQDE26'                                # IAM S3-python-user
ENV_secret_access_key='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'

ENV_S3_bucket_for_upload = "s3-bucket-for-file-upload-dev"

ENV_mySNS = "arn:aws:sns:ap-southeast-1:183391749782:mySNSDev"
ENV_data_loaded_to_pipelineSNS ="arn:aws:sns:ap-southeast-1:183391749782:data_loaded_to_pipelineSNSDev"

"""
##  The below section is for PRODUCTION (PRD) environment only
##  
ENV_environment = "PRD"            

ENV_db_client_URL = "mongodb+srv://neurallab:esuTALuGpKLeH4zG@cluster0.co32e.mongodb.net/datalake?retryWrites=true&w=majority"
ENV_db_database = 'datalake'

ENV_region='us-east-1'

ENV_access_key_id='AKIASVMYAA2LBYBQDE26'                                # IAM S3-python-user
ENV_secret_access_key='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'

ENV_S3_bucket_for_upload = "neural-lab-excel-upload"

ENV_mySNS ='arn:aws:sns:us-east-1:183391749782:mySNS'
ENV_testFS_to_pipelineSNS ="arn:aws:sns:us-east-1:183391749782:testFS_to_pipelineSNS"
ENV_lambda_4_loaded_to_feature_selectionSNS = "arn:aws:sns:us-east-1:183391749782:lambda_4_loaded_to_feature_selectionSNS"
