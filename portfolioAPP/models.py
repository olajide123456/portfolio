from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    service = models.CharField(max_length=100)
    budget = models.CharField(max_length=100, blank=True)
    timeline = models.CharField(max_length=100, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    # Store the AI reply sent to the client
    ai_reply = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = "Contact"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"