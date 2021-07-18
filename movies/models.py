from django.db import models


class Rate(models.Model):
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    def __str__(self):
        return self.rating


class Genre(models.Model):
    genres = models.CharField(max_length=256)

    def __str__(self):
        return self.genres


class Runtime(models.Model):
    runtime = models.IntegerField(null=True)

    def __str__(self):
        return self.runtime


class Type(models.Model):
    mtype = models.CharField(max_length=128)

    def __str__(self):
        return self.mtype


class Netflix(models.Model):
    netflix = models.CharField(max_length=256)

    def __str__(self):
        return self.netflix


class Year(models.Model):
    year = models.IntegerField(null=True)

    def __str__(self):
        return self.year


class Youtube(models.Model):
    youtube = models.CharField(max_length=256)

    def __str__(self):
        return self.youtube


class Movie(models.Model):
    imdb_id = models.CharField(max_length=128)
    title = models.CharField(max_length=256)
    link = models.CharField(max_length=256)
    votes = models.IntegerField(null=True, blank=True)
    cast = models.TextField(max_length=250)
    plot = models.TextField(max_length=300)
    keywords = models.TextField(max_length=150)
    poster = models.CharField(max_length=256)

    rating = models.ForeignKey(Rate, on_delete=models.CASCADE)
    genres = models.ForeignKey(Genre, on_delete=models.CASCADE)
    runtime = models.ForeignKey(Runtime, on_delete=models.CASCADE)
    mtype = models.ForeignKey(Type, on_delete=models.CASCADE)
    netflix = models.ForeignKey(Netflix, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    youtube = models.ForeignKey(Youtube, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
