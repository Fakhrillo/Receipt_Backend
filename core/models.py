from django.db import models

# Create your models here.
class Branches(models.Model):
    name = models.CharField(max_length=150, unique=True)
    created_at = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Branches"

    def __str__(self):
        return self.name
    
class Workers(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=155, unique=True)
    branch = models.ForeignKey(Branches, on_delete=models.CASCADE)
    id_tg = models.BigIntegerField(null=True, blank=True)


    class Meta:
        verbose_name_plural = "Workers"

    def __str__(self):
        return self.name

class Checks(models.Model):
    check_num = models.CharField(max_length=255, unique=True)
    sum = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    worker = models.ForeignKey(Workers, null=True, on_delete=models.SET_NULL)
    branch = models.ForeignKey(Branches, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/')
    issubmitted = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Checks"

    def __str__(self):
        return self.check_num

class Docs(models.Model):
    doc_num = models.CharField(max_length=255, unique=True)
    sum = models.CharField(max_length=255, default=0, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    worker = models.ForeignKey(Workers, null=True, on_delete=models.SET_NULL)
    branch = models.ForeignKey(Branches, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/')
    issubmitted = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Docs"

    def __str__(self):
        return self.doc_num