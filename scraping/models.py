from django.db import models

class Source(models.Model):
    name = models.CharField(max_length=30, default="Default Source", blank=True, null=True)
    link = models.CharField(max_length=2083, default="", unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the Model."""
        return self.name


class News(models.Model):
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=2083, default="", unique=True)
    published = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, default=1)

    def __str_(self):
        """Return a string representation of the model."""
        return f"{self.title[:50]}..."
