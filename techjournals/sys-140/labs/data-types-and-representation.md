# Data Types and Representation

Part 1

When looking for my text, `"This is some sample text"`, in the hex editor, I found it easily with the `.txt` as there were very few other bits. ![image](https://user-images.githubusercontent.com/12242178/189202043-3d60e1cd-0803-4621-9d1b-dfbf3d87c40b.png)

When opening the `.pdf` file, which as a formatted file has lots of control codes, I couldn't find the sample text. However, I expect it's in-between the `stream` and `endstream` points that the editor identified.

(Top of the file, showing the `stream` text)\
![image](https://user-images.githubusercontent.com/12242178/189202275-90b0fb6d-70de-4b70-9209-c7242b7b4ff7.png)

(Bottom of the file, with `endstream`)\
![image](https://user-images.githubusercontent.com/12242178/189202561-a6eb50fe-f77e-4ddf-994d-5e48e2ea2df9.png)

There are multiple instances of `endstream`, so I believe the document also has the font and size information encoded in it as well.

The search box changes options because certain queries like `10` could be hex, decimal, or the user might want it interpreted as text.\
![image](https://user-images.githubusercontent.com/12242178/189202765-238ce826-a9bb-4272-9c67-1fa1224ed5a9.png)\
The program does ask you to prefix a specific hex value you're searching for with `0x`. If you enter something that cannot represent another type of data, the program then assumes you're searching for text.\
![image](https://user-images.githubusercontent.com/12242178/189202960-283b2205-2a45-4a0c-850b-0e93a1b6d366.png)

### Part 2

I belive the image was created with Photoshop on a Mac, as the file contains: `Adobe Photoshop CS4 Macintosh2011:01:14 14:32:2`\
![image](https://user-images.githubusercontent.com/12242178/189203690-6fb58955-61af-4215-907c-008833910a52.png)

The hidden message would appear to be: `you found the hidden words!`\
![image](https://user-images.githubusercontent.com/12242178/189203807-c117032f-7d2f-4061-97be-dabd8811f623.png)

### Part 3

The largest 8-bit number is `255`. The smallest (signed) 8-bit number is `-128`.

### Part 4

* 8-bit integer = 1 character
* 16-bit integer = 2 characters
* 24-bit integer = 3 characters
* 32-bit integer = 4 characters
* 64-bit integer = ..... 8 characters?
