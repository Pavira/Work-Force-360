# app/core/matching_config.py

# Initial radius in meters (3 km)
INITIAL_RADIUS_METERS: int = 3000

# Maximum allowed radius (20 km)
MAX_RADIUS_METERS: int = 20000

# Radius increment per attempt (2 km)
RADIUS_INCREMENT_METERS: int = 2000

# Delay between retries (seconds)
RETRY_DELAY_SECONDS: int = 40


# Total retry window (seconds)
TOTAL_RETRY_TIME_SECONDS: int = 120

# job expiry time (seconds)
JOB_EXPIRY_SECONDS: int = 30

# Total attempts derived from total time and delay
MAX_ATTEMPTS: int = TOTAL_RETRY_TIME_SECONDS // RETRY_DELAY_SECONDS
