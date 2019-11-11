from webapp.models import Team


def dict(request):
    list_path = {}
    # list1 = {"user_list": Team.objects.all()}
    list1 = ''
    for e in Team.objects.all():
        list1 += str(e.user) + (', ')
    # user_list = {"user_list": list1}
    # print(list, "LIST")
    # path_dict = request.session.get('path')
    path = request.path
    path_counter = {'path_counter': request.session.get('path')}
    without_slash = {}
    for key, value in request.session.get('path').items():
        if key == '/':
            key = 'Main Page'
        without_slash[key.replace('/', '')] = value
    keys_list = ['hey', 'hey']
    new_keys = {'lol': keys_list}
    # for key in path_counter.values():
    #     keys_list.append(key)
    # print(keys_list)
    return {'lol': without_slash}

def sessions(request):
    total = {"total": request.session.get('time_index')}
    # print(total,'Total')
    return total