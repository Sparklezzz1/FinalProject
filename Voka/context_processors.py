def user_group(request):
    is_user_group = False
    if request.user.is_authenticated:
        is_user_group = request.user.groups.filter(name='Users').exists()
    return {
        'is_user_group': is_user_group,
    }

def admin_group(request):
    is_admin_group = False
    if request.user.is_authenticated:
        is_admin_group = request.user.groups.filter(name='Admins').exists()
    return{
        'is_admin_group':is_admin_group,
    }

def doctor_group(request):
    is_doctor_group = False
    if request.user.is_authenticated:
        is_doctor_group = request.user.groups.filter(name='Doctors').exists()
    return{
       'is_doctor_group':is_doctor_group,
    }