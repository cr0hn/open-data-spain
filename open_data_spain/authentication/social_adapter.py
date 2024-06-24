# en tu archivo python personalizado, por ejemplo, myapp/allauth_strategy.py

from django.contrib.auth import get_user_model
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.db.transaction import atomic

from apps.billing.models import Plan
from apps.billing.sdk.plans import PlanNames


class ODSAccountAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request, sociallogin):
        return True

    def pre_social_login(self, request, sociallogin):
        User = get_user_model()

        # Obtener1 el correo electrónico del usuario desde los datos de GitHub
        email = sociallogin.account.extra_data.get('email')

        # Intentar buscar un usuario existente con ese correo electrónico
        try:
            user = User.objects.prefetch_related("billing_plan").get(email=email)

            # Si existe, conectar el sociallogin con el usuario existente
            sociallogin.connect(request, user)

        except User.DoesNotExist:
            # Si no existe, continuar con el proceso normal de creación de usuario
            pass

    def save_user(self, request, sociallogin, form=None):
        user = None

        with atomic():
            user = super().save_user(request, sociallogin, form)

            # Auto set the billing plan to free
            Plan.objects.create(user=user, name=PlanNames.FREE)

        return user

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.email = sociallogin.account.extra_data['email']
        user.username = user.email
        user.avatar_url = sociallogin.account.extra_data['avatar_url']

        return user
