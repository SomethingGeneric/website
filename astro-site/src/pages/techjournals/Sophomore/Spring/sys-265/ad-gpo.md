---
layout: /src/layouts/MarkdownLayout.astro
---
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

## Searching Event Logs
This was a tad tricky, even thought the underlying command is pretty logical

To dump event log, just do `Get-EventLog System`, optionally adding an `-After` argument to minimize output, like `-After 3/26`

I never quite got Searching to work the way I wanted, but for this simple example I ended up with 
`Get-EventLog System -After 3/26 | Where-Object { $_.InstanceID -eq 302 }`

I tried using `Where-Object {$_.Message -eq "..." }` and a `$_.Source` but neither really worked.