import redis

pool = redis.ConnectionPool(host='auth_redis', port=6379, db=0, max_connections=20)
