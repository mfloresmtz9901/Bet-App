import pytest
from django.db import IntegrityError
from django.db import transaction
from django.test import TestCase

from bet_app.apps.core_data.models import Competition
from bet_app.apps.core_data.models import CompetitionSeason
from bet_app.apps.core_data.models import Country
from bet_app.apps.core_data.models import Participation
from bet_app.apps.core_data.models import Team


class ParticipationTests(TestCase):
    def setUp(self):
        self.team = Team.objects.create(remote_id=1, name="Team")
        self.competition = Competition.objects.create(remote_id=1, name="Cup")
        self.season = CompetitionSeason.objects.create(
            competition=self.competition,
            year=2026,
        )

    def test_duplicate_participation_is_rejected(self):
        Participation.objects.create(season=self.season, team=self.team)
        with pytest.raises(IntegrityError), transaction.atomic():
            Participation.objects.create(season=self.season, team=self.team)

    def test_national_team_can_enter_multiple_competitions(self):
        self.team.team_type = Team.TeamType.NATIONAL
        self.team.save()
        other = Competition.objects.create(remote_id=2, name="Cup")
        other_season = CompetitionSeason.objects.create(competition=other, year=2026)
        Participation.objects.create(season=self.season, team=self.team)
        Participation.objects.create(season=other_season, team=self.team)
        assert set(self.team.participations.values_list("season_id", flat=True)) == {
            self.season.pk,
            other_season.pk,
        }

    def test_country_deletion_preserves_competition_and_participation(self):
        country = Country.objects.create(code="MX", name="Mexico")
        self.competition.country = country
        self.competition.save()
        participation = Participation.objects.create(season=self.season, team=self.team)
        country.delete()
        self.competition.refresh_from_db()
        assert self.competition.country_id is None
        assert Participation.objects.filter(pk=participation.pk).exists()

    def test_shared_team_names_and_codes_are_allowed(self):
        other = Team.objects.create(
            remote_id=2, name=self.team.name, code=self.team.code,
        )
        assert other.pk != self.team.pk
