from django.db import models

class VisitorDetection(models.Model):
    '''Contains image of detected visitor and timestamp'''
    image = models.ImageField(upload_to='pi_visitors/images/')
    detection_time = models.DateTimeField(auto_now_add=True)
    
    
