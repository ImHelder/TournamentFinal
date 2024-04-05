import random
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Tournament, Participant, Match, Sport
from django.http import Http404, HttpResponse
from .forms import TournamentForm

def index(request):
        tournaments = Tournament.objects.all()
        if request.method == 'POST':
            form = TournamentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('index')
        else:
            form = TournamentForm()
        return render(request, 'index.html', context={'tournaments': tournaments, 'form': form})
   
    
def tournamentDetail(request, tournamentId):
        tournament = get_object_or_404(Tournament, pk=tournamentId)
        participants = tournament.participants.all()
        allParticipants = Participant.objects.all()
        notParticipants = allParticipants.exclude(tournaments=tournament)
      

        matchs = Match.objects.filter(tournament=tournament)
        num_participants = tournament.participants.count()
        num_rounds = calculate_num_rounds(num_participants)
        rounds = {f"Round {i + 1}": [] for i in range(num_rounds)}

        for match in matchs:
            roundName = determine_round_name(match)
            rounds[roundName].append(match)

        print("rounds", rounds)
        return render(request, 'tournament.html', {'tournament': tournament, 'participants': participants, "notParticipants": notParticipants, 'rounds': rounds})

def add_participant(request, tournament_id):
    if request.method == 'POST':
        tournament = Tournament.objects.get(pk=tournament_id)
        participant_name = request.POST.get('participant_name')
        participant = Participant.objects.create(name=participant_name)
        tournament.participants.add(participant)
        return redirect('tournamentDetail', tournamentId=tournament_id)

def addExistingParticipantToTournament(request, tournamentId, participantId):
    try:
        if request.method == 'POST':
            participant = get_object_or_404(Participant, pk=participantId)
            tournament = get_object_or_404(Tournament, pk=tournamentId)
            tournament.participants.add(participant)
        return redirect('tournamentDetail', tournamentId=tournamentId)
    except:
        return redirect('tournamentDetail', tournamentId=tournamentId)
    
def create_matches(request, tournamentId):
    tournament = Tournament.objects.get(pk=tournamentId)
    participants = list(tournament.participants.all())

    if len(participants) % 2 != 0:
        return render(request, 'error.html', {'message': 'Le nombre de participants doit être pair.'})

    random.shuffle(participants)

    for i in range(0, len(participants), 2):
        Match.objects.create(
            tournament=tournament,
            firstParticipant=participants[i],
            secondParticipant=participants[i + 1]
        )

    tournament.isStarted = True
    tournament.save()

    return redirect('tournamentDetail', tournamentId=tournamentId)


def calculate_num_rounds(num_participants):
    num_rounds = 0
    while num_participants > 1:
        num_rounds += 1
        num_participants //= 2
    return num_rounds

def determine_round_name(match):
    round_number = match.roundNumber 
    round_name = f"Round {round_number}"
    return round_name

def updateRoundScore(request, matchId):
    match = get_object_or_404(Match, pk=matchId)
    firstParticipantScore = int(request.POST.get('firstParticipantScore'))
    secondParticipantScore = int(request.POST.get('secondParticipantScore'))

    match.firstParticipantScore = firstParticipantScore
    match.secondParticipantScore = secondParticipantScore

    if firstParticipantScore > secondParticipantScore:
        match.winner = match.firstParticipant
        afterMatch = Match.objects.filter(firstParticipant=match.secondParticipant, roundNumber=match.roundNumber + 1).first()
        if(afterMatch == None):
            afterMatch = Match.objects.create(
                firstParticipant=match.firstParticipant,
                roundNumber=match.roundNumber + 1)
        else:
            print(afterMatch)
            afterMatch.secondParticipant = match.firstParticipant
            afterMatch.save()
       
    elif firstParticipantScore < secondParticipantScore:
        match.winner = match.secondParticipant
        afterMatch = Match.objects.filter(firstParticipant=match.firstParticipant, roundNumber=match.roundNumber + 1).first()
        if(afterMatch == None):
            afterMatch = Match.objects.create(
                firstParticipant=match.secondParticipant,
                roundNumber=match.roundNumber + 1)
        else:
            print(afterMatch)
            afterMatch.secondParticipant = match.secondParticipant
            afterMatch.save()
    else:
        match.winner = None

    match.save()

    return redirect('tournamentDetail', tournamentId=match.tournament.id)