from django.contrib import admin
from django.apps import apps

# Получение всех моделей из приложения
models = apps.get_models()

# Регистрация всех моделей в админке
for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
