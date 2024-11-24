
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
sh docker-commands.sh

# Step 5: Creating Cockroach database
echo "Creating Cockroach Database and Table Schemas..."
python3 main.py

# Step 7: Load Initial Data
echo "Loading initial data into the schemas..."
python3 load_data.py

