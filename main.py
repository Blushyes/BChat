from context.__init__ import context
from core import start

# 1472871866

if __name__ == "__main__":
    # 登录
    context.login_manager.login(context.uid)

    start()
