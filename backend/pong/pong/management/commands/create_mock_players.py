from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction

from accounts.player.models import Player


class Command(BaseCommand):
    """
    `python manage.py create_mock_players <num_players>`で実行
    playerのmockを作成するコマンド
    """

    help = "Create mock data for users, players"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "num_players",
            type=int,
            default=25,
            help="The number of mock players to create",
        )

    def handle(self, *args: tuple, **kwargs: dict) -> None:
        num = kwargs["num_players"]
        created_players: set[int] = set()

        # Create users and players
        for i in range(1, num + 1):  # type: ignore
            try:
                with transaction.atomic():
                    user: User = User.objects.create_user(
                        username=f"mock{i}",
                        email=f"mock{i}@example.com",
                        password="test12345",
                    )
                    Player.objects.create(
                        user=user, display_name=f"player_{i}"
                    )
                created_players.add(i)
            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(
                        f"Failed to create mock player_{i}: {str(e)}"
                    )
                )

        if created_players:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created mock players {",".join(map(str, created_players))}"
                )
            )
