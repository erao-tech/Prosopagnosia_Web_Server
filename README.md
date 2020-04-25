# Prosopagnosia_Web_Server
The web server for the Prosopagnosia Helper System which runs on a AWS EC2 instances. 

The server is currently running here: http://52.55.117.58:5000/

This project is developed specifically for the AR Glass Vuzix Blade.

Copyright 2020 EraO Prosopagnosia Helper Dev Team, Liren Pan, Yixiao Hong, Hongzheng Xu, Stephen Huang, Tiancong Wang

Supervised by Prof. Steve Mann (http://www.eecg.toronto.edu/~mann/)

Licensed under the Apache License, Version 2.0 (the "License")


## Environment:
- Python 3.5 (or better)
- A python virtual environment (Optional)
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


- Make sure there is a SQLdatabase running and configured, the SQL database model can be find in mySQL_model folder
