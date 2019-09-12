## api generator

- this tool automatically generates python code for a rest api and corresponding api doc using swagger ui, all you've to do is provide connection string to the database and verify configuration settings

- it leverages [fastapi](https://github.com/tiangolo/fastapi), which uses and ASGI server [uvicorn](http://www.uvicorn.org/) 

- currently only postgres is supported

### setup

required : python3.6+, pip3

- ```git clone https://github.com/nsingla/api_generator.git```
- ```cd api_generator```
- install pre-requisite for psycopg2 and requirements:
```bash
sudo apt-get install libpq-dev python3-dev
pip3 install -r requirements.txt
```
- update connection string and schema for which api is to be generated in the ```settings.conf```

- generate configuration file for the api generator, the api and the model will be generated based on the settings in this conf file in next steps. this will create a file named ```api_gen.conf```
```bash
python3 conf_generator.py
```

- go through the settings in the ```api_gen.conf```, top of the  file contains the description of each setting

- run script to generate api code and model inside the ```src``` folder
```bash
python3 api_generator.py
```

- ```cd src``` (you can also move and rename the src to any location)

- the src folder has all the api code, first install library requirements:
```bash
pip3 install -r requirements.txt
```

- run the api app:
```bash
uvicorn app:app --reload
```

### notes
- support for custom select queriers(complex or simple) will be added

- support for tables with composite keys as primary key will be added

- currently table names or column names with spaces in your db are not supported by this tool, it will potentially break the code

- all fields are set to be required by default, you can modify the class files inside the ```model``` folder to set default value of fields to None, this will make those fields optional

- ```http://127.0.0.1/``` redirects to /docs by default, /docs are the swagger ui docs using which you can test all the api calls and /redoc is an alternate documentation



### sample project
if you want to look at an already generated api project, a [sample project](sample_project) is included, 

follow the readme inside it if you want to try that to see how a generated api will look like
