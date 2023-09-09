# "Lab": Telnet, NC, cURL, HTTP

## Part 1: telnet
* Command: `telnet localhost 8008`
* Web request text `GET /index.html`
* Response:
[output of the telnet command](/telnet_8008_sec260.png)

## Part 2: nc
* Command: `nc -C localhost 8008`
* Web request text:
```
OPTIONS /index.html HTTP/1.1
Host: localhost
Connection: close

```
* NOTE: The trailing newline is important????
* Response:
[output of netcat command](/nc_8008_sec260.png)

### Netcat had me really stumped
So here's some stuff I looked at to figure out why `OPTIONS` wasn't `OPTION`-ing:
* [Security StackExchange Post](https://security.stackexchange.com/questions/70561/how-to-identify-the-http-methods-supported-by-a-web-server)
* [MDN page on HTTP messages](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages)
* [MDN page on HTTP OPTIONS specifically](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS)


## Part 3: curl
* Command: `curl http://localhost:8008`
* Reponse:
[output of curl command](/curl_8008_sec260.png)