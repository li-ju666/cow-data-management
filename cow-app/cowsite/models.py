from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse



#class Cow_info(models.Model):
 #   cow_id = models.CharField(max_length=30)
  #  cow_tag = models.CharField(max_length=30)
   # slug = models.SlugField(unique=True, max_length=30)
    #created_on = models.DateTimeField(auto_now_add=True)

    #def get_absolute_url(self):
     #   return reverse('cow_detail', args=[self.slug])

    #def save(self, *args, **kwargs):
        #if not self.slug:
            #self.slug =slugify(self.cow_id)
            #super(Post, self).save(*args, **kwargs)
        
    #class Meta:
     #   ordering = ['created_on']

      #  def __unicode__(self):
       #     return self.cow_id



#class Cow_health(models.Model):
 #   status = models.CharField(max_length=30)
  #  DIM = models.CharField(max_length=30)
   # text = models.TextField()


