# Forge: Our Own Proprietary Code-Sharing Platform

## Description
Forge is a robust, secure, and proprietary platform designed for seamless code collaboration and sharing within your organization. Built with a focus on efficiency, security and customizability! 

# Installation
### Grabbing the Files
  1. Make you sure you have Git Installed and Configured
  2. Clone the Reposistory with the command  ```
    git clone https://github.com/Edspeedy1/Data-Management-Systems-Project.git
    ```
### Python Set-Up | Windows
  Install the Latest Python3 version through the website, https://www.python.org/downloads/ (Be Sure to add Python to your envorimental variables)
    
  
### Python Set-Up | Linux
1. Install the Latest Python3 version through the command ```sudo apt install python3``` (Slight variations in the command needed if using non-debian based platforms

    
## Setting Up Virtual Environment 

NOTE: The following commands should be done through your IDE terminal; for the best results use the **VS Code Terminal**.  

  ### Windows
  1. Check Python Version `python --version`
  2. Create the Virtual Environment `python -m venv venv`
  3. Enter the Virtual Environment `venv\Scripts\activate`
    
 ### Linux 
 1. Check Python Version `python3 --version`
 2. Create the Virtual Environment `python3 -m venv venv`
 3. Enter the Virtual Environment `source venv/bin/activate`
    
## Installing Packages
Use pip install to install the correct packages that are listed in the requriments.txt or manually install them with:
    ```pip install bcrypt```, ```pip install multipart``` 
    
    
    
## Running the Code
  1. Run the `Server.py` file with the `python server.py`
  2. A Link will be printed in the **VS Code Terminal**, Ctrl + Left Click to open the link in your default browser
  
## Using the Program
 1. Input a Username and Password, which will be saved to the database
 2. Perform various operations such as showing User Stats and Creating Repos
 3. Enjoy and Have Fun!
  
  
