from django.db import models


class Country(models.Model):
    code = models.CharField(max_length=6, unique=True)
    name = models.CharField(max_length=100, unique=True)
    flag = models.URLField(max_length=200, null=True, blank=True)
    deactivate = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Competition(models.Model):
    class Format(models.TextChoices):
        LEAGUE = "League", "League"
        CUP = "Cup", "Cup"
        MIXED = "Mixed", "Mixed"

    remote_id = models.IntegerField(unique=True)
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="competitions",
    )
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=50,
        choices=Format.choices,
        null=True,
        blank=True,
    )
    logo = models.URLField(max_length=200, null=True, blank=True)
    active = models.BooleanField(default=False)
    deactivate = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CompetitionSeason(models.Model):
    competition = models.ForeignKey(
        Competition,
        on_delete=models.CASCADE,
        related_name="seasons",
    )
    year = models.IntegerField()
    current = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["competition", "year"],
                name="unique_competition_season",
            ),
        ]

    def __str__(self):
        return f"{self.competition.name} - {self.year}"


class Venue(models.Model):
    remote_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=100, null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    surface = models.CharField(max_length=50, null=True, blank=True)
    altitude = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.city}"


class Team(models.Model):
    class TeamType(models.TextChoices):
        UNKNOWN = "unknown", "Unknown"
        CLUB = "club", "Club"
        NATIONAL = "national", "National"

    remote_id = models.IntegerField(unique=True)
    code = models.CharField(max_length=3, blank=True, default="")
    name = models.CharField(max_length=100)
    team_type = models.CharField(
        max_length=10,
        choices=TeamType.choices,
        default=TeamType.UNKNOWN,
    )
    logo = models.URLField(max_length=200, null=True, blank=True)
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        related_name="teams",
    )
    founded = models.IntegerField(null=True, blank=True)
    venue = models.ForeignKey(
        Venue,
        on_delete=models.SET_NULL,
        null=True,
        related_name="home_teams",
    )

    def __str__(self):
        return self.name


class Participation(models.Model):
    season = models.ForeignKey(
        CompetitionSeason,
        on_delete=models.CASCADE,
        related_name="participations",
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="participations",
    )
    active = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["season", "team"],
                name="unique_team_season_participation",
            ),
        ]

    def __str__(self):
        return f"{self.team.name} - {self.season}"
