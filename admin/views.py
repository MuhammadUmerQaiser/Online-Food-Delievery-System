from django.shortcuts import render, redirect
from functools import wraps

def indexAdmin(request):
    return render(request, 'adminIndex.html')


def authenticated_only(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not 'name' in request.session:
            return redirect('loginUser')  # Redirect to your login page
        return view_func(request, *args, **kwargs)
    return wrapped_view