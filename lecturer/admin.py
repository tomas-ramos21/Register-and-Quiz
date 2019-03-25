from django.contrib import admin
from lecturer.models import Question, Class, Teaching_Day, Published_Question, Topic

admin.site.register(Question)
admin.site.register(Class)
admin.site.register(Teaching_Day)
admin.site.register(Published_Question)
admin.site.register(Topic)
