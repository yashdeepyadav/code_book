from django.core.management.base import BaseCommand
from django.db.models import Count
from market.models import Project , Profile
from datetime import timedelta, datetime
from django.utils.timezone import utc

class Command(BaseCommand):
    help = 'Displays count of all Users and Projects created'
  
    def handle(self, *args, **kwargs):
        
  
        Projects_published = Project.objects.get().count()
        Profiles_created = Profile.objects.get().count()
  
        print("Articles Published in last 5 hours = ",
              articles_published_in_last_5_hour)
          
        print("Comments per Article in last 5 hours")
        for data in comments_published_per_article:
            print(data)