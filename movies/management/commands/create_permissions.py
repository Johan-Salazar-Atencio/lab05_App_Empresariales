from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create editores group, editor_user, and superuser'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        editor_group, created = Group.objects.get_or_create(name='editores')
        if created:
            self.stdout.write(self.style.SUCCESS('Created group: editores'))

        add_movie_perm = Permission.objects.get(codename='add_movie')
        change_movie_perm = Permission.objects.get(codename='change_movie')
        editor_group.permissions.set([add_movie_perm, change_movie_perm])
        self.stdout.write(self.style.SUCCESS('Assigned add and change permissions to editores group'))

        if not User.objects.filter(username='editor_user').exists():
            editor_user = User.objects.create_user(
                username='editor_user',
                email='editor@example.com',
                password='editor_password',
            )
            editor_user.groups.add(editor_group)
            self.stdout.write(self.style.SUCCESS('Created user: editor_user'))

        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin_password',
            )
            self.stdout.write(self.style.SUCCESS('Created superuser: admin'))

        self.stdout.write(self.style.SUCCESS('All users and groups created successfully!'))
