
#!/bin/bash

# Exit script on error
set -e

# Step 1: Create Virtual Environment
echo "Creating virtual environment..."
python3 -m venv venv

# Step 2: Activate Virtual Environment
echo "Activating virtual environment..."
source venv/bin/activate

# Step 3: Install packages
echo "Install Python Packages..."
pip install -r requirements.txt

# Step 4: Initialize docker and initalize cluster
echo "Setup Docker and Cluster Initialization..."
chmod +x docker-commands.sh
docker-compose up -d

# Step 5: "Setup Cockroach"
echo "Setting up cockroach DB Network..."
sh docker-commands.sh

# Step 6: Setup Mongo Sharding Network
echo "Creating Mongo Sharding Network..."
chmod +x mongo-setup.sh
sh mongo-setup.sh

# Step 7: Creating Cockroach database
echo "Creating Cockroach and MongoDB Database and Table Schemas..."
python3 main.py

# Step 7: Load Initial Data
echo "Loading initial data into the schemas..."
python3 load_data.py

cd fastapi_server
# Ensure that we build again so it doesn't load older image
docker-compose up --build
echo "FastAPI Server Initialized!"