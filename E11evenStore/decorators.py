from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def cliente_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'email_cliente' not in request.session:
            messages.error(request, "Debes iniciar sesión como cliente.")
            return redirect('inicio_sesion')  
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'email_admin' not in request.session:
            messages.error(request, "Debes iniciar sesión como administrador.")
            return redirect('inicio_sesion')  
        return view_func(request, *args, **kwargs)
    return wrapper
