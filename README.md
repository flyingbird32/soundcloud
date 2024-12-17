#  soundcloud autoclaimer

my attempt at creating a tool that automates claiming usernames on soundcloud by repeatedly sending requests to the soundcloud api

## preview
![preview1](https://cdn.discordapp.com/attachments/1316828170573320305/1318685062383931472/preivew.gif?ex=676338aa&is=6761e72a&hm=c683fbf2910c6f66ad7f70b5370f7bdb8108b086bbe99a6a5b4bacb6e218bd63&)

## features
- **custom headers**: preconfigured headers to emulate a legitimate browser request.
- **checks multiple usernames**: allows checking multiple usernames at the same time.
- **multiple sessions**: uses multiple sessions for improved efficiency.
- **proxy support**: works with and without proxies (proxy support is recommended).
- **discord webhook notifications**: sends a notification to a discord webhook when a claim is successful (toggleable).

## installation

1. **clone the repository**:
   
   ```bash
   git clone https://github.com/flyingbird32/soundcloud.git
   cd soundcloud
   ```
   
2. **install dependencies**:
   
   ```bash
   pip install -r requirements.txt
   ```
   
3. **execute the script in the terminal:**
   
   ```bash
   python main.py
   ```

## configuration

```json
{
    "threads": 300, // amount of threads
    "checks_per_session" : 50, // how many usernames you want to be checked at the same time
    "cooldown_after_ratelimit" : 30, 
    "log_attempts" : true, // if you want to see attempts, may perform faster if off
    "use_webhook" : false,
    "webhook_url" : ""
} 
```

## requirements
- python 3.8 or later
- pip (python package manager)

## disclaimer
this tool is for educational purposes only. unauthorized access or misuse of soundcloud's api may violate their terms of service. use responsibly.

