# Lab ?? - AD GPO

## AD Stuff in PowerShell

### Moving Objects
`Move-ADObject -Identity "DN-to-Move" -TargetPath "DN-Of-Destination-Object"`

In the case of this lab, we did `Move-ADObject -Identity "TARGOBJ" -TargetPath "OU=Software Deploy,DC=MATT,DC=LOCAL"`
With `TARGOBJ` being `CN=WKS01-MATT,CN=Computers` and `CN=Matt,CN=Users`

### Making a new OU
This one is very easy.
`New-ADOrganizationalUnit -Name "ThingieYouWant" -Path "DC=MATT,DC=LOCAL"`
In our case:
`New-ADOrganizationalUnit -Name "Software Deploy" -Path "DC=MATT,DC=LOCAL"`

### Removing OU 
This one was also pretty easy
`Remove-ADObject -Identity "OU=Test OU,DC=MATT,DC=LOCAL"`