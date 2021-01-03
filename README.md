Nimble playback script for redirect users based on black list.

# Redirection users by IP in Nimble Streamer
`Required python 3.6`

# Features
- Create IP white list users for nimle live streams.
  - By IPv4
  - By Subnetworks
  - By nimble user agent
- Redirect blocked users to another video stream

# Configuration
./Nimble-playback-script/`config.py`

### IP and port of server
```
ADDR_THIS_SERVER = 'localhost'
PORT_THIS_SERVER = 8008
```

### User agents
```
ALLOWED_USER_AGENT = [
    "allow_group",
    "Some group"
]
```

### List of IPs/Subnetworks users
```
WHITE_LIST_IP = [
    'XX.XX.XX.XX', 
    'XX.XX.XX.XX/24'
]
```

### Stream URL fo redorection user
```
REDIRECT_LOCATION = 'https://cdn.kvant.mk.ua/kvanttv/kvant-err/playlist.m3u8'
```
