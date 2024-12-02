# Geo-Distributed Supply Chain Management

## Group project for CSE 512 : Distributed Database Systems

## Group Name : Guardians of Data

## Group Member : Gaurav Bansode, Parshav Barbhaya, Suyash Sutar, Hardik Patel

**_Note_** This setup has been developed and deployed in Mac OS environment hence all the installation scripts are in .sh formate, we recommend for testing to be done in the same environment for maximum stability. Alternativly Linux can also be used for testing.

## Installation Steps:

### Pre-installation requirements:

1. `python3` installed and working (Recommended version 3.11.5 -- this is the version on author's machine)
2. `docker-desktop` This is required to simulate the multi region setup and to host APIs.
3. First time installation on a new machine requires Internet connection -- downloading libraries and artifacts
4. Make sure that `docker daemon` is running in your local.
5. Please make sure that you have required `certificates` before running the installation script as this project uses some features from CockroacDBs enterprise version.

### System Requirements:

Please make sure that other programs in your computer are closed as this project will create >15 Docker services which requires 8GB of system memory free at the minimum. We recommend testing the code in systems with 16 GB RAM.

### Configuration Steps:

1. Start Docker daemon on your machine
2. Run `. installation.sh` in the subfolder containing that file. (For Windows users pleae make sure `WSL` is installed in your local)
3. docker exec -it mongos1 mongosh --host 127.0.0.1 --port 27017
4. Copy the commands from shard_setup.js
5. Paste the commands from shard_setup in mongo console.
6. Start Postman (Alternatively you can also use SwaggerUI provided by FastAPI).
7. Import the collections from postman collections folder.
8. Start testing.

### Grafana Setup (Optional)

**_Note_** This is kept optional as the system would have more than 20 docker container running and most machine won't be able to handle it.

1. Run `docker-compose up --build` from inside the grafana_setup directory.
2. After the containers are up please add `http://loki:3100/ ` as the source to pull the logs.
3. After the source is added we can use data explorer to query the logs and find and pinpoint issues.

## Project Structure

**Info:** There are multiple folders containing specific code for each task.

1. `data_files`: This folder contains the dummy data used to simulate the multi region setup.
2. `db_connection`: Contains files to connect to the DB once it is up.
3. `db_creation`: Contains code to create the Database and corrosponding table in both CockroachDB and MongoDB.
4. `db_load_data`: Contains code to load the data in data_files into the DB.
5. `fastapi_server`: Contains docker setup and code for the FastAPI server which have APIs exposed to interact with the application.
6. `installation.sh`: This file is to be run to create a `.venv` and install the dependencies required to run disitributed database and docker containers.(it takes some time, grab a coffee!)
7. `requirements.txt`: Contains list of all the dependencies required to run this project
8. `main.py`: Main file to run the DB initialization step.
9. Project Submission will also contain submission related output and report files not available here!

## Sample working terminal example:

@TODO: Add image here
