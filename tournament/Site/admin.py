from django.contrib import admin
from .models import Tournament, Participant, Match, Sport

# Register your models here.
admin.site.register(Tournament)
admin.site.register(Participant)
admin.site.register(Match)
admin.site.register(Sport)