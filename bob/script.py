import os

with open("template.html") as f:
    inp = f.read()

add_html = ""
for f in os.listdir("."):
    if not ".html" in f and not ".py" in f:
        print("Showing " + f)
        os.system("xdg-open " + f)
        if input("Add? (Y/n): ") != "n":
            add_html += "<img src=\"" + f + "\" width=\"50%\"></img>\n"
            add_html += "<p>" + input("Comment: ") + "</p><br/>"

out = inp.replace("$ADD_PICS", add_html)

with open(input("Filename: "), "w") as f:
    f.write(out)