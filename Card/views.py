from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.forms import inlineformset_factory, formset_factory
import json
from django.template.loader import render_to_string
from .models import Module
from .utils import generate_inviteCode
from .forms import ModuleEditingForm, get_dynamic_form_class
from django.db import connection

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
    module = get_object_or_404(Module, slug=module_slug) if module_slug else None
    
    form_module = ModuleEditingForm(instance=module)
    table_name = f'Module_{module_slug}'

    form_module = ModuleEditingForm(request.POST, instance=module)
    DynamicForm = get_dynamic_form_class(table_name) 
    DynamicFormSet  = formset_factory(DynamicForm, extra=0)

    if request.method == "POST":
        if "logout" in request.POST:
            logout(request)
            return redirect('main')

        if "delete-this-module" in request.POST and module:
            module.delete()
            return redirect('user_library', user=request.user.username)

        formset = DynamicFormSet(request.POST, request.FILES, form_kwargs={'table_name': table_name})

        if form_module.is_valid() and formset.is_valid():
            module = form_module.save(commit=False)
            
            for form in formset:
                form.save()
            
            print("VALID FORMSET 123123123")

            if module_slug is None:
                module.save()
                module.user.set([request.user])

            # Возвращаем JSON-ответ для успешного выполнения
            JsonResponse({"success": True})
            return redirect('user_library', user=request.user.username)
        else:
            errors_form_module = {}
            for error_list in form_module.errors.values():
                for error in error_list:
                    errors_form_module["module"] = error
            JsonResponse({"success": False, "errors": errors_form_module}, status=400)

            errors_formset = {}
            for form_error in formset.errors:
                if isinstance(form_error, dict):
                    for field, error in form_error.items():
                        errors_formset[field] = error
            return JsonResponse({"success": False, "errors": errors_formset}, status=400)

    else:
        form_module = ModuleEditingForm(instance=module) if module else ModuleEditingForm()
        
        # Пример получения начальных данных из БД
        initial_data = []
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT type_card, word_front, word_back, phrase_front, phrase_back, image, 
                    audio_word_front, audio_word_back, audio_phrase_front, audio_phrase_back
                FROM {table_name}
                """
            )
            rows = cursor.fetchall()
            for row in rows:
                initial_data.append({
                    'type_card': row[0],
                    'word_front': row[1],
                    'word_back': row[2],
                    'phrase_front': row[3],
                    'phrase_back': row[4],
                    'image': row[5],
                    'audio_word_front': row[6],
                    'audio_word_back': row[7],
                    'audio_phrase_front': row[8],
                    'audio_phrase_back': row[9],
                })

        # Создаем FormSet, передавая initial_data и form_kwargs для передачи table_name
        formset = DynamicFormSet(
            initial=initial_data,
            form_kwargs={'table_name': table_name}
        )


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
                # flashcard = get_object_or_404(Flashcard, id=request.POST[flashcard_id])
                # flashcard.delete()

        # После удаления перенаправляем на тот же маршрут или на другой
        return redirect('user_library', user=request.user.username)  # Замените на имя вашего представления, куда нужно перенаправить

    return HttpResponse("Invalid request", status=400)
