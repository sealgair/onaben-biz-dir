from django.db import models
import random, time 


class RandomManager(models.Manager):
    def get_random(self):
        data = self.get_query_set()
        ids = []
        for item in data.all():
            for i in range(item.weight):
                ids.append(item.id)
        
        if (ids):
            random.seed(time.time())
            return self.get(id=random.choice(ids))
        else:
            return None

class BannerAd(models.Model):
    objects = RandomManager()
    
    name = models.CharField(max_length=64, null=True, default=None)
    image = models.ImageField(blank=False, upload_to="img/banners")
    hyperlink = models.URLField(blank=False)
    weight = models.IntegerField(default=1)
    
    def __unicode__(self):
        return self.name