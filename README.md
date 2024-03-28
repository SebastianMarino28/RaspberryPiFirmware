In order to automate the Raspberry Pi to collect and upload sensor data periodically on boot, the automateScripts.service and automateScripts.timer files need to be moved to the /etc/systemd/system folder.

The App folder can be placed on the desktop of the Raspberry Pi. The id field in the python programs will need to be unique to each machine so this will have to be manually entered during initial setup.

These commands will need to be ran in the terminal in order to enable the required files and activate the timer:

chmod +x runPrograms.sh

sudo systemctl daemon-reload

sudo systemctl enable automateScripts.timer


Once all of this setup is complete the SD card memory can be copied and duplicated to as many Raspberry Pi's needed. A technician would only need to change the machine ID in the python code for each unique AWG.
