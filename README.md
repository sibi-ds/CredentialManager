# Credential Management
This Application is to manage credentials within an organization

Credential Management is aiming to provide a SaaS application for managing credentials 
using Django, rest framework and Cryptography. Major purpose of the application
is to maintain credentials inorder to store and give access to the employees within the organization.
Each employee in the organization can create any no. of vaults and can give Read or Read and Write access.
The access level can be organization, project or individual level.

## Credential Management supports
- Employees, Projects
- Vaults, Components and Items
- Vault Accesses
- Organizations (Multi tenancy)

### Note :
Credential Management is still in development phase and it has to be enhanced according to the further requirements

### Installed Apps : 
Different apps created for the development are as follows. These are added to the Installed Apps
list field in **settings.py** file

- organization
- employee
- project
- credential

### setup:
- Git clone the main branch from the remote repository into the local repository
- Create a separate environment for the project parallel to the project location
- Activate the environment using {environment-name}\scripts\activate command in any Command Line Interface
- Install all the necessary packages for the project as mentioned in the requirement.txt file which is placed in the project base directory
- Use the following command to install the packages : pip install -r requirement.txt
- Mention the database details in the settings.py file in the project
- Go to the base directory and run the following command to create migration scripts for each app in the project : python manage.py makemigrations {app-name}
- Run the following command to migrate the database scripts for each app in the project : python manage.py migrate {app-name}
- Run the following command to run the project : python manage.py runserver

### folder structure
```
├── project-environment
│   └── scripts
│       └── activate.bat
└── CredentialManaget
    └── requirement.txt
    └── CredentialManager
        └── settings.py
```