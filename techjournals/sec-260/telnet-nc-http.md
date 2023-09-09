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

## Part 3: curl
* Command: `curl http://localhost:8008`
* Reponse:
[output of curl command](/curl_8008_sec260.png)