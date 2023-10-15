def is_delegate():
    import persistent.base as persistent
    from config import config
    return persistent.MarkStrategy.DELEGATE == config.get_persistent_config('strategy')