import random
from typing import Final

from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.player.models import Player
from matches import constants
from matches.match.models import Match
from matches.participation.models import Participation as MatchParticipation
from matches.score.models import Score
from tournaments.participation.models import (
    Participation as TournamentParticipation,
)
from tournaments.round.models import Round
from tournaments.tournament.models import Tournament

COMPLETED: Final[str] = constants.MatchFields.StatusEnum.COMPLETED.value


class Command(BaseCommand):
    """
    `python manage.py create_mock_games`で実行
    トーナメント関連のmockを作成するコマンド
    - tournament1つ
    - tournamentに参加する4人のplayerがランダムで選択される
    - tournament participations4つ
    - round2つ。statusはcompleted
    - round1はmatch2つ・round2はmatch1つ
    - match participations6つ
    - score(ランダムで一方が勝つまで作成)
    - 勝者が決定され、is_win=Trueになる
    """

    help = "Create mock data for tournaments, rounds, matches, participations, and scores"

    def handle(self, *args: tuple, **kwargs: dict) -> None:
        try:
            with transaction.atomic():
                # tournament作成
                tournament: Tournament = self._create_tournament()

                # tournamentに参加する4人のplayerをランダムに選択
                players: list[Player] = list(Player.objects.order_by("?")[:4])

                # tournamentとplayerを紐づけるtournament participationsを作成
                self._create_tournament_participations(tournament, players)

                # 1ラウンド目を作成
                round1: Round = self._create_round(tournament, 1)

                # 1ラウンド目のmatchを作成
                match1: Match = self._create_match(round1)
                match2: Match = self._create_match(round1)

                # 1ラウンド目のmatchに参加するplayerを設定
                match1_players: list[Player] = players[:2]
                match2_players: list[Player] = players[2:]

                # 1ラウンド目のmatchとplayerを紐づけるmatch participationsを作成
                match1_participations: list[MatchParticipation] = (
                    self._create_match_participations(match1, match1_players)
                )
                match2_participations: list[MatchParticipation] = (
                    self._create_match_participations(match2, match2_players)
                )

                # 1ラウンド目のmatchのscoreを作成
                self._create_scores_for_match(match1_participations)
                self._create_scores_for_match(match2_participations)

                # 1ラウンド目の勝者を決定
                match1_winner: Player = self._determine_winner(
                    match1_participations
                )
                match2_winner: Player = self._determine_winner(
                    match2_participations
                )

                # 2ラウンド目を作成
                round2: Round = self._create_round(tournament, 2)

                # 2ラウンド目のマッチを作成
                final_match: Match = self._create_match(round2)

                # 2ラウンド目のマッチに1ラウンド目の勝者を設定
                final_match_participations: list[MatchParticipation] = (
                    self._create_match_participations(
                        final_match, [match1_winner, match2_winner]
                    )
                )

                # 2ラウンド目のマッチのスコアを作成
                self._create_scores_for_match(final_match_participations)

                # 2ラウンド目の勝者を決定
                self._determine_winner(final_match_participations)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created mock tournament id={tournament.id}"
                )
            )
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"Failed to create mock tournament: {str(e)}")
            )

    def _create_tournament(self) -> Tournament:
        return Tournament.objects.create(status=COMPLETED)

    def _create_tournament_participations(
        self, tournament: Tournament, players: list[Player]
    ) -> list[TournamentParticipation]:
        participations: list[TournamentParticipation] = []
        for player in players:
            participation = TournamentParticipation.objects.create(
                tournament=tournament,
                player=player,
                participation_name=player.display_name,
            )
            participations.append(participation)
        return participations

    def _create_round(
        self, tournament: Tournament, round_number: int
    ) -> Round:
        return Round.objects.create(
            tournament=tournament, round_number=round_number, status=COMPLETED
        )

    def _create_match(self, round: Round) -> Match:
        return Match.objects.create(round=round, status=COMPLETED)

    def _create_match_participations(
        self, match: Match, players: list[Player]
    ) -> list[MatchParticipation]:
        match_participations: list[MatchParticipation] = []
        for player in players:
            participation = MatchParticipation.objects.create(
                match=match,
                player=player,
                team="1",
            )
            match_participations.append(participation)
        return match_participations

    def _create_scores_for_match(
        self, participations: list[MatchParticipation]
    ) -> None:
        scores: dict = {participation: 0 for participation in participations}
        while max(scores.values()) < 5:
            participation = random.choice(participations)
            Score.objects.create(
                match_participation=participation,
                pos_x=random.randint(0, 800),
                pos_y=random.randint(0, 600),
            )
            scores[participation] += 1

    def _determine_winner(
        self, participations: list[MatchParticipation]
    ) -> Player:
        scores = {
            participation: Score.objects.filter(
                match_participation=participation
            ).count()
            for participation in participations
        }
        winner = max(scores, key=lambda p: scores[p])
        winner.is_win = True
        winner.save()
        return winner.player
