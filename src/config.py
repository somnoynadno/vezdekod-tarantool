import os

tarantool_host = os.environ.get("TARANTOOL_HOST", "localhost")
tarantool_port = int(os.environ.get("TARANTOOL_PORT", 3301))
