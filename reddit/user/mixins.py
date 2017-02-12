from .models import ThreadKarmaPoints, CommentKarmaPoints

class UserDataMixin:
    
    def get_context_data(self, *args, **kwargs):
        context = super(UserDataMixin, self).get_context_data(*args, **kwargs)
        user = self.kwargs['username']
        thread_karma = ThreadKarmaPoints.objects.filter(user__username=user, has_voted=True)
        comment_karma = CommentKarmaPoints.objects.filter(user__username=user, has_voted=True)
        context['user'] = user
        context['thread_karma'] = thread_karma.count()
        context['comment_karma'] = comment_karma.count()
        return context