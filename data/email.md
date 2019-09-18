please find here [https://www.dropbox.com/<wbr>sh/c28qls9ueywwiar/<wbr>AACLI7XYcSLAD65s7P8H90m1a?dl=0](https://www.dropbox.com/sh/c28qls9ueywwiar/AACLI7XYcSLAD65s7P8H90m1a?dl=0)<wbr> the file 20190328ProjectStatus.zip with the latest data from the prvoius student.

First setps are:

- If required: install Ubuntu on your computer using WUBI.exe under Windows to have it available like a Windows program (But for your task it might be enough to run everything under Windows and later test under Linux on the real system)

- Install ZABBIX on your computer (database behind can be any but suggested is PostgreSQL

- Get used to ZABBIX

- Play with maps under ZABBIX

- Test the existing scripts  in 20190328ProjectStatus.zip: important is, that you do not to always create the background image and the map new. Create a map and just set or remove the antenna positions

- Create a host group WETTZELL and dynamically set the position of Wettzell 

- Read the schedule files: for International VLBI Service (IVS) you find them here [ftp://cddis.gsfc.nasa.<wbr>gov/pub/vlbi/ivscontrol/<wbr>master19.txt](ftp://cddis.gsfc.nasa.gov/pub/vlbi/ivscontrol/master19.txt) and for European VLBI Network (EVN) you find a sample attached to the email

- Select a date and time and try to set all antenna positions from the schedule file individual of the network IVS or EVN for this date and current time. The acronyms of the antennas are explained  here [https://ivscc.gsfc.nasa.<wbr>gov/about/org/components/ns-<wbr>list.html.](https://ivscc.gsfc.nasa.gov/about/org/components/ns-list.html)

Btw each station is a host group in ZABBIX and just by putting the position of an icon with this host group ZABBIX prepares all status highlighting.

If you want to use Google maps instead, we need to define how to get data out of zabbix and I can give you access to the productive system to read the status. But I would suggest to first stay in ZABBIX itself.

I heard that the last student laptop is in use. So we have no other at the moment. If you need one, please let me know and I try to arrange something. But maybe you can do the work also on your computer.