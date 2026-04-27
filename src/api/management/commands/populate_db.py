from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import Note
import random

User = get_user_model()


class Command(BaseCommand):
    help = "Seed database with users and notes"

    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            type=int,
            default=3,
            help="Number of users to create"
        )

        parser.add_argument(
            "--notes",
            type=int,
            default=10,
            help="Number of notes to create"
        )

        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing data before seeding"
        )

    def handle(self, *args, **options):
        users_count = options["users"]
        notes_count = options["notes"]
        reset = options["reset"]

        self.stdout.write("Starting seed process...")

        # reset
        if reset:
            self.stdout.write("Clearing existing data...")
            Note.objects.all().delete()
            User.objects.all().delete()

        # Create users
        users = []
        for i in range(users_count):
            user = User.objects.create_user(
                username=f"user{i}"
            )
            users.append(user)

        self.stdout.write(f"{len(users)} users created.")

        #  Create notes
        notes = []
        for i in range(notes_count):
            owner = random.choice(users)

            note = Note.objects.create(
                owner=owner,
                title=f"Note {i}",
                content="Sample content"
            )

            # Share with random users (excluding owner)
            possible_users = [u for u in users if u != owner]

            if possible_users:
                shared = random.sample(
                    possible_users,
                    k=random.randint(0, len(possible_users))
                )
                note.shared_with.set(shared)

            notes.append(note)

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed complete: {len(notes)} notes created."
            )
        )