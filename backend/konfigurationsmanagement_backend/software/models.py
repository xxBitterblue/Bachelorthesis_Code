from django.db import models


class Software(models.Model):
    name = models.CharField(max_length=30)
    version = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    dependency_software = models.ManyToManyField('self', symmetrical=False)

    def as_json(self):
        return {
            'software_id': self.id,
            'name': self.name,
            'version': self.version,
            'type': self.type,
            'dependency_software': [software.as_dep_json() for software in self.dependency_software.all()],
        }
    def as_dep_json(self):
        return {
            'software_id': self.id,
            'name': self.name,
            'version': self.version,
            'type': self.type
        }
    def as_example_json(self):
        return {
            'name': self.name,
            'version': self.version,
            'type': self.type,
            'dependency_software': [],
        }


class ImmutableSoftware(Software):
    def save(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

    class Meta:
        proxy = True
