class NotImplementException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('未实现的方法', *args)