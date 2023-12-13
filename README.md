# ACE_RATING

**Instructions for setting up database**

**To Run Code**
  1) Make sure the database is all set up and you have ignition set up
  2) Download all of the necessary files. Make sure all of the files are in the same directory on your computer. Take the files in the folder "data" and put them in the same working directory as ace.py
  3) Run ace.py through your terminal with the command "python ace.py"
**Cole section**
Make sure they name database **"Capstone"** this just needs to be initially installing pgadmin then your code should build the tables etc
** Instructions for Installing PGAdmin4 and PostgreSQL on MacOS**
  1) Search PostGRE SQL on google
  2) Click on www.postgresql.org
  3) Follow steps to download newest supported version for your OS
  4) Save ZIP file in downloads folder
  5) Follow installation steps
  6) Do not change any information
  7) When prompted with password, just type in "password". It is bad if you forget this so make it easy. If its complex, just write it down somewhere.
  8) Keep port number as default
  Now for PGAdmin:
  1) WWW.pgadmin.org
  2) Press donwload for the operating system you are using
  3) Grab the .dmg file. It is the biggest one.
  4) Download to your downloads folder
  5) Open it
  6) Follow install steps
  7) Open PGAdmin4 and follow instructions on how to create a database

**For our code to work you need to create a Database on the left side of PGAdmin.
YOU MUST NAME IT "Capstone" for our code to work with no changed. After you have created a database called "Capstone" (Case sensitivity matters), you should be good to go.**

**Instructions for installing Ignition**

  1) To install Ignition go to [https://inductiveautomation.com/downloads/]
  2) Select "Download for Mac" This will be displayed as "Download for Windows" if using Windows operating system (same process for any operating system)
  3) Fill out the form for registration - The fields required are First Name, Last Name, Role(Use "Job Seeker/Student") email, phone number, country, and integrator (Select "Yes"). **Company name** You can use "Wabash College" or anything else you like.
  4) Direct the download to where you want the files downloaded, I recommend "Desktop" but anything is fine
  5) Open your file once the download is complete and follow the instructions steps
  6) You will be prompted with an are you sure you want to open -> click "Open" or "Allow"
  7) After that you will be greeted with the "ignition installer" Follow the steps
  8) For installation options all you need is "typical"
  9) After the installation is complete you should be directed by your default browser to **Select which edition to install**
  10) Select "Maker edition"
  11) Read and agree to terms and conditions
  12) You will then be prompted to **Activate License**
  13) From here in a new tab open the link in "Need help finding your key"
  14) Select sign up at the bottom and fill out all prompts
  15) Find your verification email in the email you gave and verify your account
  16) When directed back to your account click -> **Maker Edition** -> **Get License** and accept -> copy your **License Key** direct back to the ignition installer and paste it into the license key.
  17) Create a User for your gateway (this can be anything **you will remember**)
  18) Configure ports - You can leave all the ports to the defaulted options
  19) Finish setup and start gateway
  20) Download file ACEapplication.gwbk
  21) From your gateway navigate to the left side menu to **Config** -> **Backup and Restore** -> **Restore** and then choose file and select the ACEapplication.gwbk file and hit restore
  22) Once that process is complete 
  23) On the home screen of the gateway navigate to **Run it** -> **View Projects** -> And click **Launch Project** under ACE MVP Rating
  24) **Enjoy!**
