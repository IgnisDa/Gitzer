from django.db import models
from django.utils.translation import gettext as _


class Repository(models.Model):
    path = models.CharField(
        help_text=_("The absolute path to the local git repository."), max_length=500
    )
    created_on = models.DateTimeField(
        help_text=_("The date and time this repository was logged on."),
        auto_now_add=True,
    )

    def __str__(self):
        return f"Repository in {self.path}"
