def is_delegate():
    import persistent.base as persistent
    from context.__init__ import context
    return persistent.MarkStrategy.DELEGATE == context.config_manager.get_config('persistent', 'strategy')


def get_global_config(item: str):
    from context.__init__ import context
    from context.config import DefaultConfig
    context.config_manager.get_config(DefaultConfig.GLOBAL, item)
