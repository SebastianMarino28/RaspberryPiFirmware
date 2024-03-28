In order to automate the Raspberry Pi to collect and upload sensor data periodically on boot, the automateScripts.service and automateScripts.timer files need to be moved to the /etc/systemd/system folder.

These commands will need to be ran in the terminal in order to enable the required files and activate the timer:
chmod +x runPrograms.sh
sudo systemctl daemon-reload
sudo systemctl enable automateScripts.timer
