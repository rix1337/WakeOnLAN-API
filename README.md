#  WakeOnLAN-API

[![PyPI version](https://badge.fury.io/py/wol-api.svg)](https://badge.fury.io/py/wol-api)
[![Github Sponsorship](https://img.shields.io/badge/support-me-red.svg)](https://github.com/users/rix1337/sponsorship)

A simple http interface to send wake on LAN commands. Just send a `POST` to `/FF:FF:FF:FF:FF:FF` where `FF:FF:FF:FF:FF:FF` is the desired MAC address of the device to be woken up.

# Setup

`pip install wol_api`

# Run

` wol_api --port=8080`

# Docker
```
docker run -d \
  --name="WakeOnLAN-API" \
  -p port:8080 \
  rix1337/docker-wol-api:latest
  ```
