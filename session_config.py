# Additional Pyrogram Session Configuration
# Add these to your config.py to improve stability

# Connection timeouts and retry settings
CONNECTION_TIMEOUT = 30  # seconds
READ_TIMEOUT = 60       # seconds
WRITE_TIMEOUT = 60      # seconds
CONNECT_RETRIES = 3     # number of retries
RETRY_DELAY = 5         # seconds between retries

# Session management
MAX_CONCURRENT_TRANSMISSIONS = 1  # Limit concurrent operations
SLEEP_THRESHOLD = 10              # Auto-sleep on FloodWait
SESSION_START_DELAY = 3           # Delay between starting sessions

# Network optimization
WORKERS = 4                       # Number of worker threads
PARSE_MODE = "html"              # Default parse mode

# Error handling
IGNORE_ERRORS = [
    "USER_DEACTIVATED",
    "USER_DEACTIVATED_BAN", 
    "AUTH_KEY_UNREGISTERED",
    "SESSION_REVOKED"
]

# Rate limiting protection
FLOOD_WAIT_THRESHOLD = 60        # Max flood wait time to handle
MAX_RETRIES_ON_FLOOD = 3         # Max retries on flood wait

# Proxy settings (if needed for connection issues)
# PROXY = {
#     "scheme": "socks5",
#     "hostname": "127.0.0.1",
#     "port": 1080,
#     "username": "username",
#     "password": "password"
# }
