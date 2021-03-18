from django.http import Http404
from software.models import Software
from django.shortcuts import get_list_or_404, get_object_or_404

class SoftwareService:

    def get_all(self):
        return get_list_or_404(Software)

    def add(self, name, version, type, dependency_software):
        software = Software(name=name, version=version, type=type)
        software.save()

        if len(dependency_software) > 0:
            self.fill_dependency_list(software, dependency_software)

        return software

    def delete(self, id):
        software = get_object_or_404(Software, pk=id)
        software.delete()
        return True

    def update(self, id, name, version, type, dependency_software):
        software = get_object_or_404(Software, pk=id)
        software.name = name
        software.version = version
        software.type = type
        software.save()

        software.dependency_software.clear()
        self.fill_dependency_list(software, dependency_software)

        return software

    def fill_dependency_list(self, software, dependency_software):
        for curr_software in dependency_software:
            id = curr_software["software_id"]
            try:
                s = get_object_or_404(Software, pk=id)
                software.dependency_software.add(s)
            except Software.DoesNotExist:
                raise Http404("Dependency could not be found with id:" + str(id))
