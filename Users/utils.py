from random import sample
import string
from .models import InviteCodeDb

def generate_inviteCode(user):
    code = ''.join(sample((string.ascii_letters + string.digits), 10))
    
    invite, created = InviteCodeDb.objects.get_or_create(
        user=user,
        defaults={'invite_code': code}
    )
    return invite
    

    

