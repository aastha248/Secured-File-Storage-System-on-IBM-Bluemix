# Secured File Storage System on IBM Bluemix

Name : Aastha Gupta <br>
Email : aastha.gupta@mavs.uta.edu <br>
Affiliation : University of Texas at Arlington <br>
Website URL :  <br>

## Project Description : <br>

A utility to provide "Storage as a Service" which will securely store and retrieve files to a cloud service provider. The application offers the following service to a user : <br>

1. Bluemix service contains "folders", one for original files (*.org) and one folder for backups (*.bak). <br>
2. A user can send the (local) files *.org to Bluemix. <br>
3. Allow a user to input an Encryption Key. Encrypt each file (user uploaded, on BlueMix) with simple DES.<br>
4. Allow a user to send additional files, and encrypt each. If the file name matches an already existing file name, move the original file to the backup folder.<br>
5. Handle multiple versions of the same file. <br>
6. Show the list of files and sizes, stored on Bluemix. <br>
7. Decrypt and download remote files using the key. <br>
6. Allow user to delete all *.org Bluemix files, then move the *.bak files to the originals folder. <br>


## Run the app locally <br>

1. [Install Python][] <br>
2. Download and extract the starter code from the Bluemix UI <br>
3. cd into the app directory <br>
4. Run `python server.py` <br>
5. Access the running app in a browser at http://localhost:7000 <br>

## Runn the app on bluemix using 'cf push <application_name>' on Command Line. <br>

[Install Python]: https://www.python.org/downloads/