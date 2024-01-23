# Web Terms

* HTML - HyperText Markup Language (defines how websites are made)
* URL - Universal Record Locator (unique identifier for a web resource)
* HTTP - HyperText Transfer Protocol (how HTML gets from a server to your browser)
* Static webpage - Contents are the same no matter who views the page, where, or how
* Dynamic webpages - Change based on things like a user account, active device, theme preferences etc
* Server-side scripting is a process to create dynamic HTML pages, on the server rather than being modified by the client's web browser
* Client-side scripting allows changes to happen to a dynamic webpage at the request of the client, without talking to a server. For example, switching a site to dark mode doesn't need a request to the server that initially sent the page.

### HTML Terms

* Tag: a tag is the generic element of HTML, they are surrounded by `<>`'s, and sometimes have a closing component like `</....>`
* Attributes modify a tag, for example: `<p id="something">Text</p>` where `id` is the attribute
* Forms are a collection of HTML tags to get data from the user, for example:

```html
<form action="/action_page.php">
  <label for="fname">First name:</label><br>
  <input type="text" id="fname" name="fname" value="John"><br>
  <label for="lname">Last name:</label><br>
  <input type="text" id="lname" name="lname" value="Doe"><br><br>
  <input type="submit" value="Submit">
</form> 
```

* Query strings are modifiers to a url, to change the page content
* Parameter is a name for a variable, and value is the content

