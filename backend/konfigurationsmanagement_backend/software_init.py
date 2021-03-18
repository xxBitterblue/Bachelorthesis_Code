from debian_parser import PackagesParser
import sys

class Software:
    def __init__(self):
        self.id = -1
        self.type = ""
        self.name = ""
        self.dependency_software = []
        self.dependency_software_list = []
        self.version = ""
        pass

    def __str__(self):
        return f'Software: {self.name} - {self.version} ({self.type}) {[x.name for x in self.dependency_software]}'

    def as_dep_json(self):
        return {
            'name': self.name,
            'version': self.version,
            'type': self.type,
        }
    def as_json_model(self):
        return {
            "model": "software.software",
            "pk": self.id,
            "fields": {
                'name': self.name,
                'version': self.version,
                'type': self.type,
                'dependency_software': [software.id for software in self.dependency_software if self.id not in software.dependency_software],
            }
        }
    def as_json(self):
        return {
            'name': self.name,
            'version': self.version,
            'type': self.type,
            'dependency_software': [software.as_dep_json() for software in self.dependency_software],
        }

def parse_package(file):
    package = open(file, "r", encoding="utf8").read()

    parser = PackagesParser(package)
    data = parser.parse()
    software_list = []

    for idx, meta_data in enumerate(data):
        software = Software()
        software.id = idx+10
        for key in meta_data:
            if key["tag"] == 'Package':
                software.name = key["value"]
            if key["tag"] == 'Version':
                software.version = key["value"]
            if key["tag"] == 'Section':
                software.type = key["value"]
            if key["tag"] == 'Build-Depends':
                software.dependency_software_list = key["value"].split(',')
        if len([ele for ele in software_list if ele.type == software.type]) <= 10:
            software_list.append(software)

    for software in software_list:
        for dependency_software in software.dependency_software_list:
            for ele in software_list:
                if ele.name == dependency_software.split()[0]:
                    if software.name not in ele.dependency_software_list:
                        software.dependency_software.append(ele)
                        break

    f = open("software_list.json", "w")
    f.write("[")
    for idx, s in enumerate(software_list):
        if idx == 0:
            f.write(s.as_json_model().__str__().replace("'", '"'))
        else:
            f.write(',')
            f.write(s.as_json_model().__str__().replace("'", '"'))

    f.write("]")
    f.close()

if __name__ == "__main__":
    parse_package(sys.argv[1])