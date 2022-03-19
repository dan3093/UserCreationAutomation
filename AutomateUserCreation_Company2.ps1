Import-Module activedirectory

$OFS = "`r`n"

$newuserfile = Import-Csv -Path ".\newusers_network.csv"

foreach ($User in $newuserfile)
{
    $Username 	= $User.username
	$Password 	= $User.password
	$Firstname 	= $User.'First name'
	$Lastname 	= $User.'Last Name'
	$OU 		= $User.OU
    $email      = $User.emailaddress
    $jobtitle   = $User.'Job title'
    $department = $User.Department
    $company    = $User.Company
    $telephone  = $User.'Direct Number'

    
            #Check to see if the user already exists in AD
	if (Get-ADUser -F {SamAccountName -eq $Username})
	{
		 #If user does exist, give a warning
		 Write-Warning "A user account with username $Username already exist in Active Directory."
	}
	else
	{
		#User does not exist then proceed to create the new user account
        Write-Host "$Username does not exist, creating account..." -ForegroundColor Green
    }


    Write-Host "
    Username:  $Username
    Password: $Password
    First Name: $Firstname
    Last Name: $Lastname
    OU: $OU"
    


    $OFS

      #Account will be created in the OU provided by the $OU variable read from the CSV file
		New-ADUser `
            -SamAccountName $Username `
            -UserPrincipalName "$email" `
            -Name "$Firstname $Lastname" `
            -GivenName $Firstname `
            -Surname $Lastname `
            -Enabled $True `
            -DisplayName "$Firstname $Lastname" `
            -Path $OU `
            -Company $company `
            -OfficePhone $telephone `
            -EmailAddress $email `
            -Title $jobtitle `
            -Department $department `
            -AccountPassword (convertto-securestring $Password -AsPlainText -Force) -ChangePasswordAtLogon $False

        New-Item -Path \\ntdc01.networktransusa.local\Private\ -Name "$Username" -ItemType "directory"
        $ACL = Get-ACL -Path "\\<FileServerName>\Private\$Username"
        $AccessRule = New-Object System.Security.AccessControl.FileSystemAccessRule("$Username", "Modify", "ContainerInherit, ObjectInherit", "None", "Allow")
        $ACL.SetAccessRuleProtection($true,$true)
        $ACL.SetAccessRule($AccessRule)
        $ACL | Set-Acl -Path "\\<FileServerName>\Private\$Username"
        (Get-ACL -Path "\\<FileServerName>\Private\$Username").Access | Format-Table IdentityReference, FileSystemRights, AccessControlType, IsInherited, InheritanceFlags -AutoSize

}
