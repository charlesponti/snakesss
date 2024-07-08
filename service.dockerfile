# Use the base image provided by AWS for Lambda with Python 3.10
FROM public.ecr.aws/lambda/python:3.10

# Copy our lambda function and any other required files/folders to the container
COPY src/app.py .

# Command can be lambda_handler or any other function you'd like to execute by default
CMD ["src.app.lambda_handler"]
