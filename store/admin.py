from django.contrib import admin
from .models import Book, UserBookRelation


# admin.site.register(Book)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
  pass


@admin.register(UserBookRelation)
class UserBookRelationAdmin(admin.ModelAdmin):
  pass
