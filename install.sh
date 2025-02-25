#!/bin/bash

sudo systemctl stop phinteract
sudo rm -rf /opt/phinteract
sudo mv /var/log/phinteract.csv /var/log/phinteract.csv.bck


# Crea la directory per il server
sudo mkdir -p /opt/phinteract
sudo cp phinteract.py /opt/phinteract/
sudo chmod +x /opt/phinteract/phinteract.py

# Crea il file di log
sudo touch /var/log/phinteract.csv && sudo chmod 666 /var/log/phinteract.csv
# sudo cp -s /var/log/phinteract.csv ./phinteract.csv

# Copia il file di servizio systemd
sudo cp phinteract.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable phinteract
sudo systemctl start phinteract

# Imposta la rotazione dei log
# sudo cp phinteract.logrotate /etc/logrotate.d/phinteract

echo "Installazione completata! Il server è in esecuzione."