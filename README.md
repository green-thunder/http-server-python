# HTTP Server in Python

An HTTP/1.1 server built from scratch on raw TCP sockets, as part of the CodeCrafters "Build your own HTTP server" challenge. No web framework: request parsing, routing and responses are written by hand.

## Features

- One thread per client, so several connections are served at once
- `GET /` returns `200 OK`
- `GET /echo/<text>` returns `<text>` as `text/plain`
- `GET /user-agent` returns the client's `User-Agent` header
- `GET /files/<name>` serves a file from `--directory`, or `404` if it does not exist
- `POST /files/<name>` saves the request body to `--directory` and returns `201 Created`

## Run

```bash
pipenv install
pipenv run python3 -m app.main --directory /tmp/files
```

The server listens on `localhost:4221`:

```bash
curl -i localhost:4221/echo/hello
curl -i -A "my-client" localhost:4221/user-agent
curl -i --data "hi" localhost:4221/files/note.txt
curl -i localhost:4221/files/note.txt
```

## Limitations

This is a learning project. It reads at most 1 KB per request and does not sanitize file paths, so do not expose it to an untrusted network.
