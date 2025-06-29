from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.text import slugify


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=54)
    surname = models.CharField(max_length=54)
    email = models.EmailField()

    def full_name(self):
        return f"{self.name} {self.surname}"

    def __str__(self):
        return self.full_name()


class Tag(models.Model):
    caption = models.CharField(max_length=19)

    def __str__(self):
        return f'{self.caption}'


class Post(models.Model):
    title = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=150)
    image = models.ImageField(upload_to='posts', null=True)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='tags')
    link = models.URLField(max_length=300, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"'{self.title}' by {self.author}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    text = models.TextField(max_length=330)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')



