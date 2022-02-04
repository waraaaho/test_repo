FROM public.ecr.aws/lambda/python:3.6

# Copy function code
COPY lambda.py ${LAMBDA_TASK_ROOT}
COPY ENV_definitions.py ${LAMBDA_TASK_ROOT}
COPY feature_selection.py ${LAMBDA_TASK_ROOT}
COPY getEncodedData.py ${LAMBDA_TASK_ROOT}
COPY getSchema.py ${LAMBDA_TASK_ROOT}

# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY requirements.txt  .

RUN pip3 install --upgrade pip
RUN pip3 --no-cache-dir install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda.lambda_handler" ] 