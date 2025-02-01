from random import sample
import string
from .models import InviteCodeDb

def generate_inviteCode(user):
    code = ''.join(sample((string.ascii_lowercase + string.digits), 4))
    
    invite_code, created = InviteCodeDb.objects.get_or_create(
        user=user,
        defaults={'invite_code': code}
    )
    return invite_code
    

    

