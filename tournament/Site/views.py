import random
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Tournament, Participant, Match
from .forms import TournamentForm
from django.db.models import Sum


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

        ranking = []
        for index, participant in enumerate(participants, start=1):
            total_score = Match.objects.filter(tournament=tournament, winner=participant).aggregate(total_score=Sum('firstParticipantScore') + Sum('secondParticipantScore'))['total_score']
            total_score = total_score if total_score is not None else 0
            ranking.append({'participant': participant, 'total_score': total_score})

        sorted_ranking = sorted(ranking, key=lambda x: x['total_score'], reverse=True)

        for index, item in enumerate(sorted_ranking, start=1):
            item['position'] = index

        return render(request, 'tournament.html', {'tournament': tournament, 'participants': participants, "notParticipants": notParticipants, 'rounds': rounds, "ranking": ranking[::-1]})

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

    if len(participants) !=4:
        return render(request, 'error.html', {'message': 'Le nombre de participants doit être de 4.'})

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

    if firstParticipantScore == secondParticipantScore:
        return render(request, 'error.html', {'message': 'Il ne peut pas y avoir une égalité.'})

    match.firstParticipantScore = firstParticipantScore
    match.secondParticipantScore = secondParticipantScore

    print("matchnumber", match.roundNumber)
    if firstParticipantScore > secondParticipantScore:
        match.winner = match.firstParticipant
        if(match.roundNumber == 1):
            afterMatch = Match.objects.filter(tournament=match.tournament,roundNumber=match.roundNumber + 1).first()
            print("premier",afterMatch)
            if(afterMatch == None):
                afterMatch = Match.objects.create(
                    tournament=match.tournament,
                    firstParticipant=match.firstParticipant,
                    roundNumber=match.roundNumber + 1)
            else:
                print(afterMatch)
                afterMatch.secondParticipant = match.firstParticipant
                afterMatch.save()
        else:
            Tournament.objects.filter(pk=match.tournament.id).update(isDone=True)

    elif firstParticipantScore < secondParticipantScore:
        match.winner = match.secondParticipant
        if(match.roundNumber == 1):
            afterMatch = Match.objects.filter(tournament=match.tournament,roundNumber=match.roundNumber + 1).first()
            print("deuxieme",afterMatch)
            if(afterMatch == None):
                afterMatch = Match.objects.create(
                    tournament=match.tournament,
                    firstParticipant=match.secondParticipant,
                    roundNumber=match.roundNumber + 1)
            else:
                print(afterMatch)
                afterMatch.secondParticipant = match.secondParticipant
                afterMatch.save()
        else:
            Tournament.objects.filter(pk=match.tournament.id).update(isDone=True)
    else:
        match.winner = None

    match.save()

    return redirect('tournamentDetail', tournamentId=match.tournament.id)