import json

from django.http import HttpResponse
from django.views import View
from django.contrib.contenttypes.models import ContentType

from .models import Like


class LikesView(View):
    model = None
    like_type = None

    # https://evileg.com/en/post/246/

    def get(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        # GenericForeignKey does not support get_or_create
        try:
            likedislike = Like.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, user=request.user)
            if likedislike.like is not self.like_type:
                likedislike.like = self.like_type
                likedislike.save(update_fields=['like'])
                result = True
            else:
                likedislike.delete()
                result = False
        except Like.DoesNotExist:
            obj.likes.create(user=request.user, like=self.like_type)
            result = True

        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.likes.likes().count(),
                "dislike_count": obj.likes.dislikes().count(),
                "sum_rating": obj.likes.sum_rating()
            }),
            content_type="application/json"
        )
