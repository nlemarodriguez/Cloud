#!/bin/bash
cd /home/ec2-user/venv_Grupo01/bin
source activate
export MAIN_URL="http://54.174.167.225:8080"
export BD_DESIGN="designmatch"
export BD_DESIGN_HOST="database-1.cjy24azleai9.us-east-1.rds.amazonaws.com"
export BD_DESIGN_PASSWORD="Hencho00"
export BD_DESIGN_USUARIO="admin_postgres"
export EMAIL_DESIGN_KEY="AKIASIH5IUK47FQZOPL3"
export EMAIL_DESIGN_SECRET_KEY="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"
export EMAIL_DESIGN_USER="n.lema@uniandes.edu.co"
cd /home/ec2-user/Grupo01
python3 /home/ec2-user/Grupo01/image_process.py
