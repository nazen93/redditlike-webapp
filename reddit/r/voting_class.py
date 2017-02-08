from django.db.models import Q, F, Value

from .models import Voter

class Voting_function:
    '''
    Method voting_function takes models' names as an arguments and creates voter object, as well updates the following fields : rating, up_votes, down_votes, voted.
    '''
    def voting_function(self, primary_model_variable, secondary_model_variable):   
            object_pk = self.kwargs['pk']
            direction = self.kwargs['direction']
            post_object = primary_model_variable.objects.filter(pk=object_pk)
            if not post_object:
                post_object = secondary_model_variable.objects.filter(pk=object_pk)
            voter_object = Voter.objects.filter(vote_id=object_pk, user_id=self.request.user.id)
            voter_object_up = Voter.objects.filter(vote_id=object_pk, user_id=self.request.user.id, voting_direction='up')
            voter_object_down = Voter.objects.filter(vote_id=object_pk, user_id=self.request.user.id, voting_direction='down')
            voter_object_none = Voter.objects.filter(vote_id=object_pk, user_id=self.request.user.id, voting_direction='empty')
    
            if direction == "up" and voter_object_up.exists():      
                post_object.update(rating=F('rating') - 1, up_votes=F('up_votes') - 1)           
                voter_object.update(voting_direction='empty')
            elif direction =='up' and voter_object_down.exists():
                post_object.update(rating=F('rating') + 2, up_votes=F('up_votes') + 1, down_votes=F('down_votes') - 1)
                voter_object.update(voting_direction='up')
            elif direction =='up' and voter_object_none.exists():
                post_object.update(rating=F('rating') + 1, up_votes=F('up_votes') + 1)
                voter_object.update(voting_direction='up')
            elif direction=="up":
                post_object.update(rating=F('rating') + 1, up_votes=F('up_votes') + 1)
                voted_object = Voter.objects.create(vote_id=object_pk, user_id=self.request.user.id, voting_direction=direction)
                post_object.update(voted=voted_object)
            elif direction=='down' and voter_object_up.exists():
                post_object.update(rating=F('rating') - 2, down_votes=F('down_votes') + 1, up_votes=F('up_votes') - 1)
                voter_object.update(voting_direction='down')
            elif direction=='down' and voter_object_down.exists():
                post_object.update(rating=F('rating') + 1, down_votes=F('down_votes') - 1)
                voter_object.update(voting_direction='empty')
            elif direction =='down' and voter_object_none.exists():
                post_object.update(rating=F('rating') - 1, down_votes=F('down_votes') + 1)
                voter_object.update(voting_direction='down')
            elif direction=='down':
                post_object.update(rating=F('rating') - 1, down_votes=F('down_votes') + 1)
                voted_object = Voter.objects.create(vote_id=object_pk, user_id=self.request.user.id, voting_direction=direction)
                post_object.update(voted=voted_object)
