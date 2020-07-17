# Steps to create project from scratch:
### 1. Open cmd
### 2. wsl
### 3. conda create -n PaulEnv python=3.7
### 4. conda activate PaulEnv
### 5. cd /mnt/d/PaulFetchUPCCode/
### 6. sudo apt-get install tesseract-ocr
### 7. pip install Flask-RESTful
### 8. pip install zbar-py
### 9. pip install pytesseract
### 10. pip install requests
### 11. pip install pandas
### 12. git init
### 13. git remote add origin https://github.com/abhranil-datascience/PaulFetchUPCCode.git
### 14. git pull origin master
### 15. mkdir fetchupccode
### 16. Open Atom and add project folder i.e. PaulFetchUPCCode created in step 5
### 17. Create a new python file fetchupccode.py inside PaulFetchUPCCode/fetchupccode
### 18. Add the python contents in this file.
### 19. cd /mnt
### 20. sudo mkdir tmp
### 21. sudo chmod 777 tmp
### 22. Creare a new file fetchupccode.wsgi inside PaulFetchUPCCode/fetchupccode
### 23. Add wsgi contents in this file.
### 24. cd /mnt/d/PaulFetchUPCCode/fetchupccode/
### 25. python fetchupccode.py
### 26. Test in soap ui if everything works correctly or not
### 27. cd /mnt/d/PaulFetchUPCCode
### 28. git add .
### 29. git commit -m "Code Running Successfully in Local"
### 30. git push origin master

# Instructions to deploy in cloud.

### 1. Open Aws management console --> Click on EC2 --> On the left hand side click on Key Pairs under Network and Security.
### 2. Give a name "PaulFetchUPCCodeKey" and select ppk and click on CreateKeyPair. Save the downloaded ppk file in a proper location.
### 3. Go to Instances --> Click on Launch Instances --> Search for Ubuntu and click on "Ubuntu Server 18.04 LTS (HVM), SSD Volume Type - ami-02d55cb47e83a99a0 (64-bit x86) / ami-0dc22784499f24efc (64-bit Arm)" --> Click on t2.micro --> Click on Next:Configure Instance Details --> Click on Next: Add Storage --> Click on Next: Add tags --> Click on Next: Configure Security group --> Click on Add rule and add 2 new row one for http and another for https (keep everything else same) --> Click on review and launch --> Click on Launch --> In the key pair dialog box select PaulFetchUPCCodeKey. Click on I acknowledge and then click on Launch Instances.--> Finally go to Instances page to check progress.
### 4. Open Putty --> Go to ssh --> auth and browse the PaulFetchUPCCodeKey --> Go to data under sonnection and in Auto-login username enter ubuntu --> go to session and add the public dns of the instance --> click on open --> click yes in putty security alert. you habe now successfully entered in the remote instance.
### 5. sudo apt-get update
### 6. sudo apt-get install apache2
### 7. sudo apt-get install libapache2-mod-wsgi
### 8. sudo apt-get install python-pip
### 9. sudo apt-get install tesseract-ocr
### 10. sudo pip install Flask-RESTful
### 11. sudo pip install zbar-py
### 12. sudo pip install pytesseract
### 13. sudo pip install requests
### 14. sudo pip install pandas
### 15. sudo mkdir -m 1777 /mnt/tmp
### 16. cd ~
### 17. git clone https://github.com/abhranil-datascience/PaulFetchUPCCode.git
### 18. cd PaulFetchUPCCode/
### 19. mv fetchupccode /home/ubuntu/fetchupccode
### 20. cd ../
### 21. rm -rf PaulFetchUPCCode/
### 22. sudo ln -sT ~/fetchupccode /var/www/html/fetchupccode
### 23. sudo vi /etc/apache2/sites-enabled/000-default.conf and paste the below contents just after DocumentRoot

### WSGIDaemonProcess fetchupccode threads=5
### WSGIScriptAlias / /var/www/html/fetchupccode/fetchupccode.wsgi

### <Directory fetchupccode>
###    WSGIProcessGroup fetchupccode
###    WSGIApplicationGroup %{GLOBAL}
###    Order deny,allow
###    Allow from all
### </Directory>

### 24. sudo service apache2 restart
### 25. tail -1000f /var/log/apache2/error.log
### 26. Open Soapui change the url to match the public dns and test.

