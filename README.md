# JUMPING-JIVE-Geodetic-Observatory-Wettzell

# Task 5: Dynamic ZABBIX maps

ZABBIX supports maps to show relationships between components monitored or to show locations of components on background images. These images are quite helpful to identify issues. 
Usually, these maps are static setups showing facilities of companies and so on. Because VLBI sessions include different locations and antennas, it would be valuable to dynamically change the maps. It would be especially interesting for world maps showing the telescopes of the current session and their states. As ZABBIX monitoring sets can completely be changed using the API based on JSON-RPC 2.0, it should be possible to adapt maps or create new maps (see https://www.zabbix.com/documentation/3.2/manual/api). 



What to do? 

A ZABBIX installation should be used to dynamically adapt and change ZABBIX maps with a world map as background to add and delete telescope positions. 
Single tasks:
* Install Ubuntu Linux as Windows Wubi installation 
* Install ZABBIX on Linux 
* Understand ZABBIX 
* Understand the ZABBIX API 
* Write a program or script to create a new map and to add or delete a telescope position 


[Collection of Tools](https://graphite.readthedocs.io/en/latest/tools.html)


## Setup environment:

#### Install Docker *Using the convenience script*

    # Install Docker using the dokcer script
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh


    # Allow your user to access the Docker CLI without needing root access.
    sudo usermod -aG docker $USER


#### Install Docker Compose

We’re going to install Docker Compose using PIP instead of the pre-compiled binary on GitHub because it runs a [little bit faster](/blog/docker-tip-74-curl-vs-pip-for-installing-docker-compose) (both are still Python apps).


    # Install Python and PIP.
    sudo apt-get install -y python python-pip

    # Install Docker Compose into your user's home directory.
    pip install --user docker-compose



#### Verify Everything Works


    # You should get a bunch of output about your Docker daemon.
    # If you get a permission denied error, close + open your terminal and try again.
    docker info

    # You should get back your Docker Compose version.
    docker-compose --version


# Steps for running

1.  Open Terminal and clone git repo, then run the command
`git clone https://github.com/IslamAlam/JUMPING-JIVE-Geodetic-Observatory-Wettzell.git`
`cd JUMPING-JIVE-Geodetic-Observatory-Wettzell`

2\. Now, run the docker compose microserver, run the command

`docker-compose up -d`

or if you prefer logs to be shown, then

`docker-compose up`

3\. Now access Zabbix UI at port 8090(replace this port with your port if you have changed in above compose file).  Open this URL in the browser

Postgres Server

[http://localhost:8080](http://localhost:8080/)

Zabbix

[http://localhost:8090](http://localhost:8090/)


Grafana

[http://localhost:3000](http://localhost:3000/)

Flask

[http://localhost:5000](http://localhost:5000/)


4\. Now login by entering the username & password for default Admin user with credentials.




## Reference Links

Observing Program
Master Files
https://ivscc.gsfc.nasa.gov/program/master.html


Station location
https://ivscc.gsfc.nasa.gov/stations/config/ns/


List of all station session

https://ivscc.gsfc.nasa.gov/sessions/stations/


http://www.aoc.nrao.edu/software/sched/catalogs/stations_RDBE.dat


http://www.aoc.nrao.edu/software/sched/catalogs/stations.dat

Evaluation of software packages (for system monitoring) 
http://www.jive.eu/jumpingjive/lib/exe/fetch.php?media=wiki:jumping_jive_d8.4.pdf

[Trying to use Worldmap with JSON location source](https://community.grafana.com/t/trying-to-use-worldmap-with-json-location-source-unsuccessfully/14637)


# JUMPING JIVE
[JUMPING JIVE Website](https://jive.eu/jumping-jive)

JUMPING JIVE: Joining up Users for Maximizing the Profile, the Innovation and Necessary Globalization of JIVE

![](/sites/jive.nl/files/cms/projects/JJ-logo-no-text.jpg)

The [JUMPING JIVE project](http://jumping.jive.eu/) aims to take Very Long Baseline Interferometry ([VLBI](https://en.wikipedia.org/wiki/Very-long-baseline_interferometry#VLBI_arrays "Opens in new window: https://en.wikipedia.org/wiki/Very-long-baseline_interferometry#VLBI_arrays")) <link>into the next decade, with [JIVE](http://www.jive.eu) <link>and the European VLBI Network ([EVN](http://www.evlbi.org/intro/intro.html "Opens in new window: http://www.evlbi.org/intro/intro.html")) <link>as globally recognized centres of excellence in radio astronomy.

The project brings together scientists and engineers to define the future of VLBI for scientific applications, and identify the required technological innovation to realise such a future. The project work packages cover a number of topics, which include encouraging existing telescopes to join the EVN, connecting with future instruments ([Square Kilometre Array](http://skatelescope.org/ "Opens in new window: http://skatelescope.org/"), African VLBI Network), and finding new JIVE partners to expand the membership base. In addition, there are resources for a dedicated outreach effort.

JIVE <link>is leading the project from its base in Dwingeloo (the Netherlands). Twelve institutes <link>from eight different European countries have teamed up in JUMPING JIVE. The project was awarded nearly 3 million euros, over a period of 4 years, by the Horizon 2020 Framework Programme of the EU.

<span style="font-size: 11pt">Detailed information on the project can be found on the JUMPING JIVE [web](http://jumping.jive.eu/) and</span> [wiki](/jumpingjive/doku.php?id=start "Opens in new window: https://jive.eu/jumpingjive/doku.php?id=start")<span style="font-size: 11pt"> </span> 


![](/sites/jive.nl/files/cms/projects/EU.jpg)

This project has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No 730884

More information [here](http://cordis.europa.eu/project/rcn/207184_en.html "Opens in new window: http://cordis.europa.eu/project/rcn/207184_en.html")