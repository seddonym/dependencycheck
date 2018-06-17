from layers.domain import complaints


def view(request):
    return complaints.get_complaint()
