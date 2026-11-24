from django.db import migrations, models
from django.db.models import Count, F
import django.db.models.deletion


def validate_participations(apps, schema_editor):
    participation = apps.get_model("core_data", "LeagueParticipation")
    rows = participation.objects.using(schema_editor.connection.alias)
    if rows.exclude(league_id=F("season__league_id")).exists():
        raise ValueError(
            "Participation league differs from its season. Resolve before migrating."
        )
    if (
        rows.values("season_id", "team_id")
        .annotate(total=Count("id"))
        .filter(total__gt=1)
        .exists()
    ):
        raise ValueError(
            "Duplicate team/season participations. Resolve before migrating."
        )


def restore_leagues(apps, schema_editor):
    participation = apps.get_model("core_data", "Participation")
    rows = participation.objects.using(schema_editor.connection.alias)
    for row in rows.select_related("season").iterator():
        rows.filter(pk=row.pk).update(league_id=row.season.competition_id)


class Migration(migrations.Migration):
    dependencies = [
        ("core_data", "0002_country_league_leagueparticipation_seasons_teams_and_more")
    ]

    operations = [
        migrations.RunPython(validate_participations, migrations.RunPython.noop),
        migrations.RenameModel("League", "Competition"),
        migrations.RenameModel("Seasons", "CompetitionSeason"),
        migrations.RenameModel("Teams", "Team"),
        migrations.RenameModel("LeagueParticipation", "Participation"),
        migrations.RemoveConstraint("competitionseason", "unique_league_season"),
        migrations.RenameField("competitionseason", "league", "competition"),
        migrations.AddConstraint(
            "competitionseason",
            models.UniqueConstraint(
                fields=("competition", "year"), name="unique_competition_season"
            ),
        ),
        migrations.AlterField(
            "participation",
            "league",
            models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="participations",
                to="core_data.competition",
            ),
        ),
        migrations.RunPython(migrations.RunPython.noop, restore_leagues),
        migrations.RemoveField("participation", "league"),
        migrations.AddConstraint(
            "participation",
            models.UniqueConstraint(
                fields=("season", "team"), name="unique_team_season_participation"
            ),
        ),
        migrations.AlterField(
            "competition",
            "country",
            models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="competitions",
                to="core_data.country",
            ),
        ),
        migrations.AlterField("competition", "name", models.CharField(max_length=100)),
        migrations.AlterField(
            "competition",
            "type",
            models.CharField(
                blank=True,
                null=True,
                max_length=50,
                choices=[("League", "League"), ("Cup", "Cup"), ("Mixed", "Mixed")],
            ),
        ),
        migrations.AlterField("venue", "name", models.CharField(max_length=150)),
        migrations.AlterField("team", "name", models.CharField(max_length=100)),
        migrations.AlterField(
            "team", "code", models.CharField(blank=True, default="", max_length=3)
        ),
        migrations.AddField(
            "team",
            "team_type",
            models.CharField(
                max_length=10,
                default="unknown",
                choices=[
                    ("unknown", "Unknown"),
                    ("club", "Club"),
                    ("national", "National"),
                ],
            ),
        ),
    ]
