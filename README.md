# scoped
don't mess this Manager and QuerySet, easily add scopes to your django models

## usage

### install scoped:
`pip install scoped` and add scoped to your `INSTALLED_APPS`

###add scoped to your models

```python
from django.db import models
from scoped import ScopedModel

class Article(ScopedModel):
    
    title = models.CharField(max_length=255)
    published = models.BooleanField(default=False)
    has_comments = models.BooleanField(default=False)
    
    class Scopes:
    
        @staticmethod
        def published(qs):
            return qs.filter(published=True)
        
        @staticmethod
        def drafts(qs):
            return qs.filter(published=False)

        @staticmethod
        def with_comments(qs):
            return qs.filter(has_comments=True)
```

### use your scopes

```python
Article.objects.published()

Article.objects.with_comments().published()
```
