from django.db import models
from datetime import date

# Create your models here.


class shortened_link(models.Model):
    pure_link = models.CharField(max_length=300)  # user's link to short
    comment = models.CharField(null=True, max_length=200) # description to link. can be null
    shortened_link = models.CharField(max_length=30) # shortened token
    pub_date = models.DateTimeField("date published") # date of the link's creation 
    expire_date = models.DateTimeField(null=True) # link will be expired on this date if user wants
    is_valid = models.BooleanField(default=True) 
    password = models.CharField(max_length=100, default="")
    times_used = models.IntegerField(default=0) 
    one_time = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment : {self.comment}, link : {self.shortened_link}"