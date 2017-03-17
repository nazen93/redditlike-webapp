from django.db.models import Q, F, Value

from .models import Voter
from user.models import ThreadKarmaPoints, CommentKarmaPoints

class VotingClass:
    '''
    Method voting_function takes models' names as an arguments and creates voter object, as well updates the following fields : rating, up_votes, down_votes, thread_karma, comment_karma.
    '''
    def voting_function(self, primary_model_variable, secondary_model_variable):   
            object_pk = self.kwargs['pk']
            direction = self.kwargs['direction'] #voting direction
            post_object = primary_model_variable.objects.filter(pk=object_pk)
            if post_object: #checks if the primary_model queryset is not empty, if False, then it assigns secondary_model_variable to post_object
                post_object2 = primary_model_variable.objects.get(pk=object_pk)
                if hasattr(post_object2, 'title'): #determines if the given object is a thread or a comment
                    post_or_reply = 'thread'   
                else:    
                    post_or_reply = 'comment'
            else:
                post_or_reply = 'comment'
                post_object = secondary_model_variable.objects.filter(pk=object_pk)
                post_object2 = secondary_model_variable.objects.get(pk=object_pk)
                
            voter_object = Voter.objects.filter(vote_id=object_pk, user_id=self.request.user.id)
            voter_object_up = Voter.objects.filter(vote_id=object_pk, user_id=self.request.user.id, voting_direction='up')
            voter_object_down = Voter.objects.filter(vote_id=object_pk, user_id=self.request.user.id, voting_direction='down')
            voter_object_none = Voter.objects.filter(vote_id=object_pk, user_id=self.request.user.id, voting_direction='empty')
            thread_karma = ThreadKarmaPoints.objects.filter(user=post_object2.author, voter=self.request.user)
            comment_karma = CommentKarmaPoints.objects.filter(user=post_object2.author, voter=self.request.user)
    
            if direction == "up" and voter_object_up.exists():      
                post_object.update(rating=F('rating') - 1, up_votes=F('up_votes') - 1)           
                voter_object.update(voting_direction='empty')                
                if post_or_reply == "thread":
                    thread_karma.update(has_voted=False)
                else:
                    comment_karma.update(has_voted=False)
                    
            elif direction == 'up' and voter_object_down.exists():
                post_object.update(rating=F('rating') + 2, up_votes=F('up_votes') + 1, down_votes=F('down_votes') - 1)
                voter_object.update(voting_direction='up')
                if post_or_reply =="thread":
                    thread_karma.update(has_voted=True)
                else:
                    comment_karma.update(has_voted=True)
                    
            elif direction == 'up' and voter_object_none.exists():
                post_object.update(rating=F('rating') + 1, up_votes=F('up_votes') + 1)
                voter_object.update(voting_direction='up')
                if post_or_reply =='thread':
                    thread_karma.update(has_voted=True)
                else:
                    comment_karma.update(has_voted=True)
                    
            elif direction == "up":
                post_object.update(rating=F('rating') + 1, up_votes=F('up_votes') + 1)
                voted_object = Voter.objects.create(vote_id=post_object2.id, user_id=self.request.user.id, voting_direction=direction)                                
                if not thread_karma.exists() and post_or_reply == 'thread':
                    ThreadKarmaPoints.objects.create(user=post_object2.author, voter=self.request.user, has_voted=True)
                elif not comment_karma.exists() and post_or_reply =='comment':
                    CommentKarmaPoints.objects.create(user=post_object2.author, voter=self.request.user, has_voted=True)

            elif direction == 'down' and voter_object_up.exists():
                post_object.update(rating=F('rating') - 2, down_votes=F('down_votes') + 1, up_votes=F('up_votes') - 1)
                voter_object.update(voting_direction='down')
                if post_or_reply=="thread":
                    thread_karma.update(has_voted=False)
                else:
                    comment_karma.update(has_voted=False)
           
            elif direction == 'down' and voter_object_down.exists():
                post_object.update(rating=F('rating') + 1, down_votes=F('down_votes') - 1)
                voter_object.update(voting_direction='empty')
                
            elif direction == 'down' and voter_object_none.exists():
                post_object.update(rating=F('rating') - 1, down_votes=F('down_votes') + 1)
                voter_object.update(voting_direction='down')
                
            elif direction == 'down':
                post_object.update(rating=F('rating') - 1, down_votes=F('down_votes') + 1)
                voted_object = Voter.objects.create(vote_id=post_object2.id, user_id=self.request.user.id, voting_direction=direction)
                if not thread_karma.exists() and post_or_reply == 'thread':
                    ThreadKarmaPoints.objects.create(user=post_object2.author, voter=self.request.user, has_voted=False)
                elif not comment_karma.exists() and post_or_reply =='comment':
                    CommentKarmaPoints.objects.create(user=post_object2.author, voter=self.request.user, has_voted=False)
