from django.db import models

# Create your models here.


class Country(models.Model):

    # Relational data
    code = models.CharField(max_length=6, unique=True, null=False)
    name = models.CharField(max_length=100, unique=True, null=False)

    # Extra Data
    flag = models.URLField(max_length=200, null=True, blank=True)

    # Logical status
    deactivate = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class League(models.Model):

    # Relational data
    remote_id = models.IntegerField(unique=True, null=False)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name='leagues')

    # Extra Data
    name = models.CharField(max_length=100, unique=True, null=False)
    type = models.CharField(max_length=50, null=True, blank=True)
    logo = models.URLField(max_length=200, null=True, blank=True)

    # API-Football Status
    active = models.BooleanField(default=False)

    # Logical status
    deactivate = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Seasons(models.Model):

    # Relational data
    league = models.ForeignKey(
        League, on_delete=models.CASCADE, related_name='seasons')
    year = models.IntegerField(null=False)
    current = models.BooleanField(default=False)

    # remote_id = models.IntegerField(unique=True, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['league', 'year'], name='unique_league_season')
        ]

    def __str__(self):
        return str(self.year)


class Venue(models.Model):

    # Relational data
    remote_id = models.IntegerField(unique=True, null=False)

    # Extra Data
    name = models.CharField(max_length=150, unique=True, null=False)
    city = models.CharField(max_length=100, null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    surface = models.CharField(max_length=50, null=True, blank=True)
    altitude = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.city}"


class Teams(models.Model):

    # Relational data
    remote_id = models.IntegerField(unique=True, null=False)
    code = models.CharField(max_length=3, unique=True, null=False)

    # Extra Data
    name = models.CharField(max_length=100, unique=True, null=False)
    logo = models.URLField(max_length=200, null=True, blank=True)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, related_name='teams')
    founded = models.IntegerField(null=True, blank=True)
    venue = models.ForeignKey(
        Venue, on_delete=models.SET_NULL, null=True, related_name='home_teams')


class LeagueParticipation(models.Model):

    # Relational data
    league = models.ForeignKey(
        League, on_delete=models.CASCADE, related_name='participations')
    season = models.ForeignKey(
        Seasons, on_delete=models.CASCADE, related_name='participations')
    team = models.ForeignKey(
        Teams, on_delete=models.CASCADE, related_name='participations')

    # Status
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.league.name} - {self.season.year}"
