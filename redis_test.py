import redis

def database_init():
    r = redis.Redis(host='localhost', port=6379, db=0)
    return r




if __name__ == '__main__':
    red = database_init()
    b = red.zrank('test1', '中文')
    print(b)
    c = red.zrank('test1', '中文2')
    print(c)