import sys
from app.core.security import pwd_context
try:
    print(pwd_context.hash('password123'))
except Exception as e:
    import traceback
    traceback.print_exc()
