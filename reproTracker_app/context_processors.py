from .models import *

def user_info(request):
    if request.session.get('user_authenticated'):
        user_cin = request.session.get('user_cin')
        user = Doctorant.objects.get(cin=user_cin)
        return {
            'user_name': user.nomComplet
        }
    return {}