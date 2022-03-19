# UserCreationAutomation
Scripts used to parse new user request email forms > Create users in active directory > import temporary credentials into Password Manager (Bitwarden)

These scripts were created to automate new user creation for two sister companies. HR/Users would fill out a new user request form which would then email their responses in raw text to the helpdesk email account.

The form would generate an email with the following template:

############################################################################

First name:      John

Last Name:       Smith

Extension:      5555

Direct Number:  555-555-5555

Fax Number:     555-555-5555

Cell Number:    555-555-5555

Desk Location:   IT Offices

Job title:       Systems Administrator

Hire Date:       YYYY-MM-DD

Role:            Employee | Contractor

Department:      IT Department

Location:        Salt Lake City, UT

Company:         Company1

Needs Key FOB:   Yes | No

Software Needed: VPN, Adobe Suite

Comments:         Send Temporary Credentials to Manager

############################################################################

These scripts will scan for new user request emails > open these emails and parse this information > create new user accounts in Active Directory. It will also produce a temporary password and import their temporary credentials to Bitwarden.




Required Packages:
	Python:
		imap_tools - https://pypi.org/project/imap-tools/#basic
		passwordgenerator - https://github.com/gabfl/password-generator-py/

	Powershell:
		Active Directory Module-  ActiveDirectory Module | Microsoft Docs

