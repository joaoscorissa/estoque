from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


def login(request):
    if request.method == 'POST':
        usuario_login = request.POST['usuario']
        senha = request.POST['senha']
        if campo_vazio(usuario_login) or campo_vazio(senha):
            messages.error(request, "Não pode ter campo vazio")
            return redirect('login')
        if User.objects.filter(email__iexact=usuario_login).exists():
            usuario = User.objects.get(email__iexact=usuario_login)
            user = auth.authenticate(username=usuario.username, password=senha)

        else:
            user = auth.authenticate(username=usuario_login, password=senha)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Acesso negado! Usuário ou senha incorreta.')
            return render(request, 'user/login.html')


def logout(request):
    auth.logout(request)
    return redirect('index')


def buscar(request):
    if request.user.is_authenticated:
        if request.user.has_perm('auth.view_user'):
            if request.method == 'GET':
                users = User.objects.filter()
                dados = {
                    'titulo': 'Usuarios - Buscar',
                    'rows': users
                }
                return render(request, 'user/buscar.html', dados)
        else:
            return redirect('/admin/')
    else:
        return redirect('/admin/')


def inserir(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            email = request.POST['email']
            username = request.POST['username']

            obj = User.objects.filter(email__exact=email).exists()
            username = User.objects.filter(username=username).exists()

            if obj:
                messages.warning(request, 'Email já cadastrado')
                return redirect('user_inserir')
            elif username:
                messages.warning(request, 'Username já cadastrado')
                return redirect('user_inserir')
            else:
                model = User.objects.create()
                model.username = request.POST['username']
                model.password = request.POST['password']
                model.first_name = request.POST['first_name']
                model.email = request.POST['email']
                model.last_name = request.POST['last_name'].upper()
                model.is_active = True
                model.groups.add(1)
                model.save()

                if model is not None:
                    messages.success(request, 'Usuario Cadastrado com sucesso!')
                    return redirect('user_buscar')
                else:
                    messages.warning(request, 'Erro ao cadastrar usuario!')
                    return redirect('user_inserir')
        elif request.method == 'GET':
            dados = {
                'titulo': 'Usuario - Inserir',
                'flag': 0
            }
            return render(request, 'user/cadastro.html', dados)
    else:
        return redirect('/admin/')


def editar(request, id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            usuario = User.objects.filter(id=id).last()
            if usuario is not None:
                dados = {
                    'titulo': 'Usuario - Atualizar',
                    'model': usuario,
                    'flag': 1
                }
                return render(request, 'user/cadastro.html', dados)
    else:
        return redirect('/admin/')


def atualizar(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            usuario = User.objects.filter(id=request.POST['id']).last()
            if usuario is not None:
                usuario.username = request.POST['username']
                if usuario.password != request.POST['password']:
                    usuario.set_password(request.POST['password'])
                usuario.first_name = request.POST['first_name']
                usuario.email = request.POST['email']
                usuario.last_name = request.POST['last_name'].upper()
                usuario.is_active = request.POST['is_active']
                usuario.groups.add(1)
                usuario.save()

                messages.success(request, 'Alterações Realizadas com Sucesso')
                if usuario.password != request.POST['password']:
                    return redirect('index')
                else:
                    return redirect('user_buscar')
            else:
                messages.warning(request, 'Ocorreu um erro ao alterar os dados deste Usuario')
                return redirect('user_buscar')
    else:
        return redirect('index')


def campo_vazio(campo):
    return not campo.strip()