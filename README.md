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
- Orgaizations (Multi tenancy)

### Note :
Credential Management is still in development phase and it has to be enhanced according to the further requirements

### Installed Apps : 
Different apps created for the development are as follows. These are added to the Installed Apps
list field in **settings.py** file

- organization
- employee
- project
- credential
