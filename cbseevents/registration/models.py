from event.models import *
from student.models import *
from .utils import *


# Create your models here.
class TransactionRecord(models.Model):
    transaction_id = models.SlugField(unique=True)
    amount = models.FloatField()
    remark = models.CharField(max_length=55, default="")
    registration_id = models.CharField(max_length=55)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = "{slug}-{count}".format(slug=self.registration_id, count=self.pk)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.transaction_id


class RegistrationRecord(models.Model):
    registration_id = models.SlugField(unique=True)
    amount = models.FloatField(default=0)
    type = models.CharField(max_length=50)
    c_o_e = models.CharField(max_length=75)
    status = models.BooleanField(default=False)
    cancel = models.BooleanField(default=False)
    transaction_id = models.ManyToManyField(TransactionRecord)
    student = models.ForeignKey(StudentRecord, on_delete=models.CASCADE)
    event = models.ForeignKey(EventRecord, on_delete=models.CASCADE)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.registration_id:
            self.registration_id = unique_slug(self, self.event)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.registration_id
