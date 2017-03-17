from .models import ThreadKarmaPoints, CommentKarmaPoints

class UserDataMixin:    
    '''
    Adds currently logged in user to the context, as well as thread karma and comment karma.
    '''
    def get_context_data(self, *args, **kwargs):
        context = super(UserDataMixin, self).get_context_data(*args, **kwargs)
        current_user = self.kwargs['username']
        thread_karma = ThreadKarmaPoints.objects.filter(user__username=current_user, has_voted=True)
        comment_karma = CommentKarmaPoints.objects.filter(user__username=current_user, has_voted=True)
        context['current_user'] = current_user
        context['thread_karma'] = thread_karma.count()
        context['comment_karma'] = comment_karma.count()
        return context