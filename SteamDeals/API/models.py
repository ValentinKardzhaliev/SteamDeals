from django.db import models


class Game(models.Model):
    app_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=200)
    discount_percent = models.IntegerField(default=0)
    final_formatted_price = models.CharField(max_length=10, blank=True, null=True)
    initial_formatted_price = models.CharField(max_length=20)
    image_url = models.URLField(blank=True, null=True)  # Assuming image URLs are stored

    def __str__(self):
        return self.name
