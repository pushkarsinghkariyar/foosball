from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


class Team(models.Model):
    player1 = models.CharField(max_length=250, null=False, blank=False)
    player2 = models.CharField(max_length=250, null=False, blank=False)
    name = models.CharField(max_length=250, unique=True, null=False, blank=False)
    id = models.AutoField
    pass

    def clean(self):
        if self.player1 == self.player2:
            raise ValidationError('Player 1 and Player 2 cannot be same')

    def __str__(self):
        return self.name


class Match(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team1")
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team2")
    team1score = models.fields.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(0)], null=False,
                                            blank=False)
    team2score = models.fields.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(0)], null=False,
                                            blank=False)
    id = models.AutoField

    def clean(self):

        if self.team1 == self.team2:
            raise ValidationError('Team 1 and Team 2 cannot be same')

        if (self.team1score == 10 or self.team2score == 10) == False:
            raise ValidationError('At least One Team Should Have Scored 10 Goals')

        if self.team1score == 10 and self.team2score == 10:
            raise ValidationError('Only one team can score 10 goals')
    # def __str__(self):
    #     return 'Match Between ' + str(self.team1.name) + ' and ' + str(self.team2.name) + '. Scores are ' + str(
    #         self.team1score) + '-' + str(self.team2score)
