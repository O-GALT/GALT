from functools import wraps

from django.core.exceptions import PermissionDenied
from core.essenciais import TipoUsuario

def nivel_acesso_permitido(tipos_permitidos: list[TipoUsuario]):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = args[0].user
            tipos_usuario = user.groups.all()

            for tipo in tipos_usuario:
                if TipoUsuario(tipo.name) in tipos_permitidos:
                    return func(*args, **kwargs)
            raise PermissionDenied
        return wrapper
    return decorator