from django.contrib import admin
from .models import Question,Choice,Article,Tag,Comment,Classification

class ArticleAdmin(admin.ModelAdmin):
    fields = ['title','classification','tags','pub_date','content']
    list_display = ['title','pub_date','modified_time','author']
    filter_horizontal = ('tags',)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(ArticleAdmin, self).save_model(request,obj,form,change)

    def relateTags(self,obj):
        return [tag for tag in obj.tags.all()]


class ArticleDetailAdmin(admin.ModelAdmin):
    list_display = ['article', 'content']


class CommentAdmin(admin.ModelAdmin):
    fields = ['article','comment_text','email','url','name']
    list_display = ['article','comment_text','comment_pub_date','name','url']

    def save_model(self, request, obj, form, change):
        obj.comment_user = request.user
        super(CommentAdmin, self).save_model(request, obj, form, change)



admin.site.register(Article,ArticleAdmin)
# admin.site.register(ArticleDetail,ArticleDetailAdmin)
admin.site.register(Tag)
admin.site.register(Classification)

admin.site.register(Comment,CommentAdmin)
admin.site.register(Question)
admin.site.register(Choice)


# Register your models here.
