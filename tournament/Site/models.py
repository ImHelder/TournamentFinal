from django.db import models

class Sport(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    participants = models.ManyToManyField('Participant', related_name='tournamentParticipants')
    isStarted = models.BooleanField(default=False)
    isDone = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Participant(models.Model):
    name = models.CharField(max_length=100)
    tournaments = models.ManyToManyField(Tournament, related_name='participantsTournaments')
    match = models.ManyToManyField('Match', related_name='participantsMatch')

    def __str__(self):
        return self.name

class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    firstParticipant = models.ForeignKey(Participant, related_name='firstParticipant', on_delete=models.CASCADE)
    secondParticipant = models.ForeignKey(Participant, related_name='secondParticipant', on_delete=models.CASCADE, null=True, blank=True, default=None)
    firstParticipantScore = models.PositiveIntegerField(default=0)
    secondParticipantScore = models.PositiveIntegerField(default=0)
    winner = models.ForeignKey(Participant, related_name='winner', on_delete=models.CASCADE, null=True, blank=True, default=None)
    roundNumber = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.firstParticipant} contre {self.secondParticipant}"