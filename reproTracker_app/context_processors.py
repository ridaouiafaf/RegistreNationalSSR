from django.core.exceptions import ObjectDoesNotExist
from .models import *

def user_info(request):
    user_cin = ""
    if request.session.get('user_authenticated'):
        user_cin = request.session.get('user_cin')
        try:
            user = Doctorant.objects.get(cin=user_cin)
            return {
                'user_name': user.nomComplet
            }
        except Doctorant.DoesNotExist:
            return {
                'user_name': None,
                'error': f'No Doctorant found with CIN: {user_cin}'
            }
    return {}
