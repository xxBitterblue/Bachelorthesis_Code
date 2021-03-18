from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField
from core_application.models import Category

from validation.ValidationExceptions.ValidationRuleException import ValidationRuleException
from validation.ValidationExceptions.ValidationRuleVersionException import ValidationRuleVersionException


class ValidationRule(models.Model):
    name = models.CharField(max_length=30)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    is_global = models.BooleanField(default=True)
    rule = models.TextField()
    categorys = models.ManyToManyField(Category, symmetrical=False)

    def as_json(self):
        return {
            "validation_rule_id": self.id,
            "name": self.name,
            "author": self.author.additionaluserinformation.as_json(),
            "active": self.active,
            "is_global": self.is_global,
            "rule": self.rule,
            "categorys": [category.as_json() for category in self.categorys.all()],
        }


class ValidationRuleDto(ValidationRule):
    class Meta:
        proxy = True

    def validate(self, software_list):
        exec(self.rule, {
            'software_list': software_list,
            'ValidationRuleException': ValidationRuleException,
            'ValidationRuleVersionException': ValidationRuleVersionException
        })
