from django.db import models


class Match(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        LIVE = "live", "Live"
        FINISHED = "finished", "Finished"
        POSTPONED = "postponed", "Postponed"
        CANCELLED = "cancelled", "Cancelled"
        ABANDONED = "abandoned", "Abandoned"

    remote_id = models.IntegerField(unique=True)
    season = models.ForeignKey(
        "core_data.CompetitionSeason",
        on_delete=models.PROTECT,
        related_name="matches",
    )
    home_team = models.ForeignKey(
        "core_data.Team",
        on_delete=models.PROTECT,
        related_name="home_matches",
    )
    away_team = models.ForeignKey(
        "core_data.Team",
        on_delete=models.PROTECT,
        related_name="away_matches",
    )
    kickoff = models.DateTimeField(null=True, blank=True, db_index=True)
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.SCHEDULED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(home_team=models.F("away_team")),
                name="match_distinct_teams",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    status__in=[
                        "scheduled",
                        "live",
                        "finished",
                        "postponed",
                        "cancelled",
                        "abandoned",
                    ],
                ),
                name="match_valid_status",
            ),
        ]

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"


class MatchTeamStatistics(models.Model):
    """Latest cumulative match totals, including extra time when played.

    NULL means unavailable; zero means a reported zero. These rows are current
    snapshots, not a history of live updates or separate period totals.
    """

    class Side(models.TextChoices):
        HOME = "home", "Home"
        AWAY = "away", "Away"

    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name="statistics",
    )
    side = models.CharField(max_length=4, choices=Side.choices)
    corners = models.PositiveIntegerField(null=True, blank=True)
    yellow_cards = models.PositiveIntegerField(null=True, blank=True)
    shots_on_target = models.PositiveIntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["match", "side"],
                name="unique_match_statistics_side",
            ),
            models.CheckConstraint(
                condition=models.Q(side__in=["home", "away"]),
                name="match_statistics_valid_side",
            ),
        ]

    def __str__(self):
        return f"{self.match} - {self.side} statistics"

    @property
    def team(self):
        if self.side == self.Side.HOME:
            return self.match.home_team
        if self.side == self.Side.AWAY:
            return self.match.away_team
        message = "Statistics side must be home or away."
        raise ValueError(message)
