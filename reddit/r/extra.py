from django.shortcuts import get_list_or_404, get_object_or_404

from datetime import date, datetime, timezone

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

class Sorting(VotedUpDown):
    '''
    Sorts the queryset based on selected sort method.
    '''    
    def sort_method(self, sort_by, category):
        if category == None: #if category is None, then the sorting won't be restricted by subforum
            if sort_by == 'new':
                sorted_queryset = PostText.objects.filter(is_active=True).order_by('-date')
                
            elif sort_by == 'top':
                sorted_queryset = PostText.objects.filter(is_active=True).order_by('-rating')
            
            elif sort_by == 'controversial':
                sorted_queryset = PostText.objects.filter(is_active=True).order_by('-comments_count')
           
            elif sort_by == 'rising':
                sorted_queryset = PostText.objects.filter(is_active=True).order_by('-rating')
                current_date = datetime.now(timezone.utc)
                for object in sorted_queryset:
                    post_added = current_date-object.date #checks how many days ago the post has been posted
                    object.added = post_added.days #adds 'added' attribute (how many days ago the post has been added)
                sorted_queryset = list(filter(lambda x:x.added < 1, sorted_queryset)) #removes posts that are older than 1 day
            
            elif sort_by == 'promoted':
                sorted_queryset = PostText.objects.filter(is_active=True, is_promoted=True).order_by('-date')
        
        else: #adds subforum filter to the query
            category_or_404 = get_list_or_404(PostText, subforum__name=category) #checks if the requested subforum exists, if false then raises 404 page not found error
            subforum_objects = PostText.objects.filter(is_active=True, subforum__name=category)
            
            if sort_by == 'new':
                sorted_queryset = subforum_objects.order_by('-date')
            
            elif sort_by == 'top':
                sorted_queryset = subforum_objects.order_by('-rating')

            
            elif sort_by == "controversial":
                sorted_queryset = subforum_objects.order_by('-comments_count')
            
            elif sort_by == 'rising':
                sorted_queryset = subforum_objects.order_by('-rating')
                current_date = datetime.now(timezone.utc)
                for object in sorted_queryset:
                    post_added = current_date-object.date 
                    object.added = post_added.days 
                sorted_queryset = list(filter(lambda x:x.added < 1, sorted_queryset)) 
           
            elif sort_by == 'promoted':
                sorted_queryset = PostText.objects.filter(is_active=True, is_promoted=True, subforum__name=category)
        
        updated_queryset = self.up_or_down(sorted_queryset) #updates the queryset with direction attribute (if the logged in user has voted)
        return updated_queryset 