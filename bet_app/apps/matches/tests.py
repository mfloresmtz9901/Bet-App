import pytest
from django.db import IntegrityError
from django.db import transaction
from django.db.models.deletion import ProtectedError
from django.test import TestCase

from bet_app.apps.core_data.models import Competition
from bet_app.apps.core_data.models import CompetitionSeason
from bet_app.apps.core_data.models import Team
from bet_app.apps.matches.models import Match
from bet_app.apps.matches.models import MatchTeamStatistics


class MatchStatisticsTests(TestCase):
    def setUp(self):
        competition = Competition.objects.create(remote_id=1, name="Cup")
        season = CompetitionSeason.objects.create(competition=competition, year=2026)
        self.home = Team.objects.create(remote_id=1, name="Home")
        self.away = Team.objects.create(remote_id=2, name="Away")
        self.match = Match.objects.create(
            remote_id=1,
            season=season,
            home_team=self.home,
            away_team=self.away,
        )

    def test_missing_values_differ_from_reported_zero(self):
        home = MatchTeamStatistics.objects.create(match=self.match, side="home")
        away = MatchTeamStatistics.objects.create(
            match=self.match,
            side="away",
            corners=0,
            yellow_cards=0,
            shots_on_target=0,
        )
        home.refresh_from_db()
        away.refresh_from_db()
        assert home.corners is None
        assert home.yellow_cards is None
        assert home.shots_on_target is None
        assert away.corners == 0
        assert away.yellow_cards == 0
        assert away.shots_on_target == 0
        assert home.team == self.home
        assert away.team == self.away

    def test_duplicate_side_is_rejected(self):
        MatchTeamStatistics.objects.create(match=self.match, side="home")
        with pytest.raises(IntegrityError), transaction.atomic():
            MatchTeamStatistics.objects.create(match=self.match, side="home")

    def test_invalid_side_is_rejected(self):
        with pytest.raises(IntegrityError), transaction.atomic():
            MatchTeamStatistics.objects.create(match=self.match, side="other")

    def test_negative_statistics_are_rejected(self):
        for field in ("corners", "yellow_cards", "shots_on_target"):
            with pytest.raises(IntegrityError), transaction.atomic():
                MatchTeamStatistics.objects.create(
                    match=self.match,
                    side="home",
                    **{field: -1},
                )

    def test_identical_teams_are_rejected(self):
        with pytest.raises(IntegrityError), transaction.atomic():
            Match.objects.filter(pk=self.match.pk).update(away_team=self.home)

    def test_invalid_status_is_rejected(self):
        with pytest.raises(IntegrityError), transaction.atomic():
            Match.objects.filter(pk=self.match.pk).update(status="other")

    def test_team_deletion_preserves_match_history(self):
        with pytest.raises(ProtectedError):
            self.home.delete()

    def test_deleting_match_removes_its_statistics(self):
        statistics = MatchTeamStatistics.objects.create(match=self.match, side="home")
        self.match.delete()
        assert not MatchTeamStatistics.objects.filter(pk=statistics.pk).exists()
