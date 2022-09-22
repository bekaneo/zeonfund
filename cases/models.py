from django.db import models

STATUS_CHOICES = (
    (1, 'Active'),
    (2, 'Success'),
    (3, 'Closed'),
    (4, 'In process of review'),

)


class Case(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.TimeField()
    created_at = models.TimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, blank=True,
                                 null=True)

    def __str__(self):
        return self.title, self.status


class Images(models.Model):
    image = models.ImageField(upload_to='cases')
    case = models.ForeignKey(Case, on_delete=models.CASCADE,
                             related_name='images')

    def __str__(self):
        return self.case
