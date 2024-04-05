from django.db import models

class SMTPConfiguration(models.Model):
    smtp_name = models.CharField(max_length=100)
    smtp_sender = models.EmailField()
    smtp_password = models.CharField(max_length=100)
    smtp_server = models.CharField(max_length=100)
    smtp_server_port = models.IntegerField()

    def __str__(self):
        return f'{self.smtp_name} - {self.smtp_sender} - {self.smtp_server}'