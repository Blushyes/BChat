class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        self.credential = ''

        # 记录session的map
        self.session_dict = {}

    def set_credential(self, credential):
        self.credential = credential

    def __str__(self) -> str:
        return f'credential: {self.credential}'


# 唯一的单例config
config = Config()
