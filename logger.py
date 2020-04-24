class Logger:
    @classmethod
    def debug(cls, msg):
        print('[DEBUG]', msg)

    @classmethod
    def error(cls, msg):
        print('[ERROR]', msg)
