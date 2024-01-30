import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.urls import reverse

User = get_user_model()
ADMIN_URL = reverse("admin:index")


class Command(BaseCommand):
    help = "generate super admin"

    # def add_arguments(self, parser):
    #     parser.add_argument('platform', nargs='+', type=str)

    def handle(self, *args, **options):
        username = os.getenv("SUPER_ADMIN_USERNAME", "admin")
        email = os.getenv("SUPER_ADMIN_EMAIL", "admin@gmail.com")
        password = os.getenv("SUPER_ADMIN_PASSWORD", "admin12345")
        try:
            if email and password:
                user = User.objects.filter(Q(email=email) | Q(username=username)).first()
                if not user:
                    try:
                        user = User(email=email, username=username)
                        user.is_active = True
                        user.is_superuser = True
                        user.is_staff = True

                        user.set_password(password)
                        user.save()
                        message = f"""
                            new superuser crediential
                            username:{username}
                            email:{email}
                            password: {password}
                        """
                        user.email_user("new super user credential", message)
                        self.stdout.write(self.style.SUCCESS("super admin created"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(e))

                elif password:
                    message = f"""
                        updated superuser crediential
                        username:{username}
                        email:{email}
                        password: {password}
                    """
                    user.set_password(password)
                    user.is_active = True
                    user.is_superuser = True
                    user.is_staff = True
                    user.email = email
                    user.username = username
                    user.save()
                    user.email_user("updated super user credential", message)
                    self.stdout.write(self.style.WARNING("super admin updated"))
                else:
                    self.stdout.write(self.style.WARNING("super admin already exists"))

            else:
                self.stdout.write(self.style.WARNING("SUPER_ADMIN_EMAIL does not exist in the enviroment variable."))
        except Exception:
            ...

        self.stdout.write(self.style.SUCCESS("done"))
