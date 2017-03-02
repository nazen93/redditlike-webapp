from .models import PostText, Voter

class VotedUpDown:
    '''
    Takes given queryset as an argument and checks if Voter object for the given record exists, if positive then adds direction attribute (either "up" or "down") to the record. Returns updated queryset.
    '''    
    def up_or_down(self, queryset):
        try:
            user = self.request.user
            for object in queryset:
                if Voter.objects.filter(user=user, vote_id=object.id, voting_direction="up").exists():
                    object.direction = 'up'
                elif Voter.objects.filter(user=user, vote_id=object.pk, voting_direction="down").exists():
                    object.direction = 'down'                       
            return queryset
        except TypeError: #if user is not logged in, the function returns unmodified queryset
            return queryset
