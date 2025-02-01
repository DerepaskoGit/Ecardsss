from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
import json
from django.template.loader import render_to_string
from .models import Module, Flashcard
from .utils import generate_inviteCode
from .forms import ModuleEditingForm, CardEditingForm

def index(request):
    user = request.user

    if request.method == "POST" and "logout" in request.POST:
        logout(request)
        return redirect('main')

    Data = {
        'this_page':'index',
        'title':'Home',
        'user': user,
    }

    return render(request, 'Card/index.html', Data)

def generate_inviteCode_view(request):
    if request.method == 'POST':
        invite = generate_inviteCode(request.user)
        return JsonResponse({'invite':invite.invite_code})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def food_view(request):
    user = request.user

    if request.method == "POST" and "logout" in request.POST:
        logout(request)
        return redirect('food')

    Data = {
        'this_page': 'food',
        'title':'Food',
        'user_isAuthenticated': user,
    }

    return render(request, 'Card/food.html', Data)


def user_library_view(request, user):
    this_user = User.objects.get(username=request.user.username)
    modules = this_user.modules.all()

    if request.method == "POST" and "logout" in request.POST:
        logout(request)
        return redirect('main')

    data = {
        'this_page': 'user_library',
        'modules':modules,
    }

    return render(request, 'Card/user_library.html', data)




def modul_view(request, module_slug=None):
    # Получаем модуль по slug, если он передан, иначе создаем новый
    module = get_object_or_404(Module, slug=module_slug) if module_slug else None

    # Создаем inline formset для карточек
    CardFormSet = inlineformset_factory(
        Module,
        Flashcard,
        form=CardEditingForm,
        extra=0,  # Мы добавляем одну пустую форму для добавления новой карточки
        can_delete=True
    )

    # Формы для модуля
    form_module = ModuleEditingForm(instance=module) if module else ModuleEditingForm()
    formset = CardFormSet(request.POST or None, instance=module) if module else CardFormSet()

    if request.method == "POST":
        # Проверка на выход из аккаунта
        if "logout" in request.POST:
            logout(request)
            return redirect('main')

        # Удаление модуля, если выбрано
        if "delete-this-module" in request.POST and module:
            module.delete()
            return redirect('user_library', user=request.user.username)

        # Обработка формы модуля и карточек
        form_module = ModuleEditingForm(request.POST, instance=module)
        formset = CardFormSet(request.POST, instance=module)

        if form_module.is_valid() and formset.is_valid():
            # Сохраняем изменения в модуле
            module = form_module.save(commit=False)
            if module_slug is None:
                module.save()
                module.user.set([request.user])

            # Привязываем карточки к модулю и сохраняем их
            formset.instance = module
            formset.save()  # Сохраняем карточки, включая новые и удаленные

            # Возвращаем JSON-ответ для успешного выполнения
            JsonResponse({"success": True})
            return redirect('user_library', user=request.user.username)

        else:
            # Если есть ошибки валидации, выводим их
            errors = {}
            for error_list in form_module.errors.values():
                for error in error_list:
                    errors["module"] = error
            for error_list in formset.errors:
                for error in error_list.values():
                    errors["flashcard"] = error

            return JsonResponse({"success": False, "errors": errors}, status=400)

    # Подготовка данных для рендеринга
    data = {
        'this_page': 'module',
        'user': request.user,
        'form_module': form_module,
        'formset': formset,
        'module_slug': module_slug,
    }

    return render(request, 'Card/module.html', data)




def delete_flashcard_view(request):
    if request.method == "POST":
        # Получаем все карточки и проверяем, какие из них нужно удалить
        for form in request.POST:
            if form.endswith("-DELETE") and request.POST[form] == "on":
                # Получаем ID карточки из поля "id"
                flashcard_id = form.replace("-DELETE", "-id")
                flashcard = get_object_or_404(Flashcard, id=request.POST[flashcard_id])
                flashcard.delete()

        # После удаления перенаправляем на тот же маршрут или на другой
        return redirect('user_library', user=request.user.username)  # Замените на имя вашего представления, куда нужно перенаправить

    return HttpResponse("Invalid request", status=400)
