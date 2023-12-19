def current_path(request):
    return {
        'current_path': request.path,
    }