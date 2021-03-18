from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField
from software.models import Software


class Category(models.Model):
    category_name = models.CharField(max_length=20)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name="children")

    def as_json(self):
        return {
            "category_id": self.id,
            "category_name": self.category_name,
            "parent": '' if self.parent is None else {
                "category_id": self.parent.id,
                "category_name": self.parent.category_name
            },
            "children": [] if len(self.children.all()) == 0 else [{
                "category_id": children.id,
                "category_name": children.category_name
            } for children in self.children.all()]
        }


class Setting(models.Model):
    deadline = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_author')
    required_users = models.ManyToManyField(User, symmetrical=False, related_name='%(class)s_required')
    categorys = models.ManyToManyField(Category, symmetrical=False)

    def as_json(self):
        return {
            'setting_id': self.id,
            'deadline': self.deadline,
            'author': self.author.additionaluserinformation.as_json(),
            'required_users': [user.additionaluserinformation.as_json() for user in self.required_users.all()],
            'categorys': [category.as_json() for category in self.categorys.all()]
        }


class UserComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    timestamp = models.DateField()

    def as_json(self):
        return {
            "user_comment_id": self.id,
            "author": self.author.additionaluserinformation.as_json(),
            "comment_text": self.comment_text,
            "timestamp": self.timestamp
        }


class ChangeHistoryEntry(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    change_reason = models.TextField(null=True)
    changes = JSONField(null=True, blank=True)
    timestamp = models.DateField()

    def as_json(self):
        return {
            "change_history_entry_id": self.id,
            "author": self.author.additionaluserinformation.as_json(),
            "changes": self.changes,
            "change_reason": self.change_reason if self.change_reason is not None else "",
            "timestamp": self.timestamp
        }


class RequirementGroup(models.Model):
    requirement_group_name = models.CharField(max_length=30, default="Anforderungsgruppe")
    status = models.BooleanField(default=False)
    status_comment = models.TextField(null=True)
    timestamp = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user_comments = models.ManyToManyField(UserComment, symmetrical=False)
    change_history = models.ManyToManyField(ChangeHistoryEntry, symmetrical=False)
    software_list = models.ManyToManyField(Software, symmetrical=False)

    def as_json(self):
        return {
            "requirement_group_id": self.id,
            "requirement_group_name": self.requirement_group_name,
            "author": self.author.additionaluserinformation.as_json(),
            "status": self.status,
            "status_comment": self.status_comment if self.status_comment is not None else "",
            "timestamp": self.timestamp,
            "category": self.category.as_json(),
            "software_list": [software.as_json() for software in self.software_list.all()],
            "user_comments": [comment.as_json() for comment in self.user_comments.all()] if len(self.user_comments.all()) > 0 else [],
            "change_history": [history_entry.as_json() for history_entry in self.change_history.all()] if len(self.change_history.all()) > 0 else []
        }


class CategoryRequirementGroup(RequirementGroup):
    reference_groups = models.ManyToManyField(RequirementGroup, symmetrical=False, related_name='%(class)s_groups')

    def as_category_group_json(self):
        json = self.as_json()
        json["reference_groups"] = [group.id for group in self.reference_groups.all()]
        return json