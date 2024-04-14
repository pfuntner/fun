# JSON format
My parser script was a nice exercise but I later discovered that the `speedtest` command has a `--format json` option:
```
$ speedtest --format json 2>/dev/null | jq
{
  "type": "result",
  "timestamp": "2024-04-14T19:28:14Z",
  "ping": {
    "jitter": 79.401,
    "latency": 35.232,
    "low": 10.769,
    "high": 91.408
  },
  "download": {
    "bandwidth": 53736775,
    "bytes": 641947632,
    "elapsed": 12713,
    "latency": {
      "iqm": 59.929,
      "low": 10.704,
      "high": 463.745,
      "jitter": 15.441
    }
  },
  "upload": {
    "bandwidth": 34696041,
    "bytes": 494559726,
    "elapsed": 14936,
    "latency": {
      "iqm": 152.199,
      "low": 9.735,
      "high": 599.903,
      "jitter": 52.022
    }
  },
  "packetLoss": 0,
  "isp": "Ting Fiber",
  "interface": {
    "internalIp": "172.28.99.175",
    "name": "eth0",
    "macAddr": "00:15:5D:AE:0B:9A",
    "isVpn": false,
    "externalIp": "64.99.222.191"
  },
  "server": {
    "id": 11814,
    "host": "speedtest.rtmc.net",
    "port": 8080,
    "name": "NeoNova (Randolph Telephone)",
    "location": "Asheboro, NC",
    "country": "United States",
    "ip": "74.206.64.18"
  },
  "result": {
    "id": "11701809-a404-4e4a-aeb4-eb85a546319c",
    "url": "https://www.speedtest.net/result/c/11701809-a404-4e4a-aeb4-eb85a546319c",
    "persisted": true
  }
}
```
