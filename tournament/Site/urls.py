from django.urls import path
from .views import index, tournamentDetail, add_participant, addExistingParticipantToTournament, create_matches, updateRoundScore

urlpatterns = [
    path('', index, name='index'),
    path('tournament/<int:tournamentId>/', tournamentDetail, name='tournamentDetail'),
    # path('tournament/<int:tournamentId>/rankings/', rankings, name='rankings'),
    # path('tournament/<int:tournamentId>/history/', history, name='history'),
    path('add_participant/<int:tournament_id>/', add_participant, name='add_participant'),
    path('add_existing_participant/<int:tournamentId>/<int:participantId>/', addExistingParticipantToTournament, name='add_existing_participant'),
    path('create_matches/<int:tournamentId>/', create_matches, name='create_matches'),
    path('update_round_scores/<int:matchId>/', updateRoundScore, name='update_round_scores')
]