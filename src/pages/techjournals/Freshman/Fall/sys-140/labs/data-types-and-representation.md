---
layout: /src/layouts/MarkdownLayout.astro
title: "Data Types and Representation"
---
# Data Types and Representation

Part 1

When looking for my text, `"This is some sample text"`, in the hex editor, I found it easily with the `.txt` as there were very few other bits. ![image](/images/github_cdn_cd934611.png)

When opening the `.pdf` file, which as a formatted file has lots of control codes, I couldn't find the sample text. However, I expect it's in-between the `stream` and `endstream` points that the editor identified.

(Top of the file, showing the `stream` text)\
![image](/images/github_cdn_968ca199.png)

(Bottom of the file, with `endstream`)\
![image](/images/github_cdn_f5fa4ea0.png)

There are multiple instances of `endstream`, so I believe the document also has the font and size information encoded in it as well.

The search box changes options because certain queries like `10` could be hex, decimal, or the user might want it interpreted as text.\
![image](/images/github_cdn_97b17f17.png)\
The program does ask you to prefix a specific hex value you're searching for with `0x`. If you enter something that cannot represent another type of data, the program then assumes you're searching for text.\
![image](/images/github_cdn_d0bbd522.png)

### Part 2

I belive the image was created with Photoshop on a Mac, as the file contains: `Adobe Photoshop CS4 Macintosh2011:01:14 14:32:2`\
![image](/images/github_cdn_77e5e628.png)

The hidden message would appear to be: `you found the hidden words!`\
![image](/images/github_cdn_e5831386.png)

### Part 3

The largest 8-bit number is `255`. The smallest (signed) 8-bit number is `-128`.

### Part 4

* 8-bit integer = 1 character
* 16-bit integer = 2 characters
* 24-bit integer = 3 characters
* 32-bit integer = 4 characters
* 64-bit integer = ..... 8 characters?
