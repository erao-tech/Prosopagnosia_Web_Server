# Prosopagnosia_Web_Server
The web server for the Prosopagnosia Helper System which runs on a AWS EC2 instances. Currently running here:
http://52.55.117.58:5000/

## Environment:
- Python 3.5 (or better)
- A python virtual environment
- Flask
- Boto3 (AWS Python SDK)
- Python MySQL connecter
- AWS CLI 

## Instruction


- Create a new python virtual environment (Optional) as follows:
```
   python -m venv venv
```
- Install Flask
```
   venv/bin/pip install flask
````
- Install AWS Command Line Interface (CLI)

   Follow instruction in https://aws.amazon.com/cli/

- Install Boto3
```
   venv/bin/pip install boto3
```

- Install python mysql connecter

```
pip install mysql-connector-python
```

- Configure aws credentials
```
   aws configure
```
- Run the app
```
   run.py
```
