class Authorization:
    class Spotify:
        client_id = "e45b1dae4b2747049b92af3a510341b3"
        client_secret = "f9fd1ffa162b4ef1b98c32b1da0b10e4"

class Color:
    neutral = 0xFF5733  # Example neutral color
    success = 0x28A745  # Example success color
    warning = 0xFFC107  # Example warning color
    danger = 0xDC3545   # Example danger color
    search = 0x007BFF   # Example search color

class Emoji:
    approve = "✅"   # Emoji for approval
    warn = "⚠️"      # Emoji for warning
    deny = "❌"      # Emoji for denial or rejection
    # Add other emojis as needed

class Cache:
    # Example attributes for cache configuration
    size = 100
    timeout = 60  # Time in seconds

cache = Cache()
