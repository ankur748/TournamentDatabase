To work on this project, issue the following command to get the repository

git clone https://github.com/ankur748/TournamentDatabase.git

Project has certain pre-requsites before we can use it. We are using postgres sql to store data of the tournament and using python as framework.

Attached a script to download and install dependencies of project in dependencies.sh for ubuntu server.

It can be changed correspondingly depending upon the OS you are working on. For eg: apt-get can be replaced with brew in Mac OS X.

After installing the dependencies, we need to create the database structure for tournament data to be stored to be used by the python app. Follow the following steps:

1. Login to psql console by typing command psql
2. Create database named "tournament" to be used by the app. It is the first command in tournament.sql
3. Switch to newly created database "tournament" by issuing the command "\c tournament"
4. Create tables and views required by copying over the sql commands from tournament.sql script apart from create database command in the same order as given in the file.

Database structure is now ready for data to be pushed and used for analysis.

tournament.py is the basic file which provides all interfaces to push data to database.

We can use the functions by importing modules of tournament.py by creating a new .py file in the same folder and importing modules using line "from tournament import *"

A test file with sample usage around the functions has been provided in tournament_test.py. You can test all your set up by issuing the command "python tournament_test.py". You should receive a Success message if everything works just fine. If not, there might be some issue in the above steps.

Please follow the usage in the same way for your app.