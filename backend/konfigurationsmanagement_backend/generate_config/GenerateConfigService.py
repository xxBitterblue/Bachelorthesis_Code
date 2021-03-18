from pathlib import Path
import yaml
import os
from core_application.models import RequirementGroup
from django.shortcuts import get_object_or_404


class GenerateConfigService:
    current_path = "~/Desktop"
    path_to_salt_states = "salt_states"
    base_dir = "salt"

    def generate(self, requirement_groups):
        group_list = [get_object_or_404(RequirementGroup, pk=group["requirement_group_id"]) for group in requirement_groups]
        top_file = {}
        states = {}

        for group in group_list:
            self.create_installed_state_dict(states, group.software_list, group.category.category_name)
            top_file['base'] = {}
            if group.category.category_name not in top_file:
                top_file['base'][f"group:{group.category.category_name}"] = [{'match': 'grain'}, self.path_to_salt_states + "." + group.category.category_name]

        Path(os.path.join(os.path.expanduser(self.current_path), self.base_dir, self.path_to_salt_states)).mkdir(parents=True, exist_ok=True)

        self.create_yaml(os.path.join(os.path.expanduser(self.current_path), self.base_dir, 'top.sls'), top_file)

        for key, val in states.items():
            self.create_yaml(os.path.join(os.path.expanduser(self.current_path), self.base_dir, self.path_to_salt_states, f'{key}.sls'), {key: val})

        return self.current_path + "/" + self.base_dir

    def create_installed_state_dict(self, state_dict, software_list, category):
        if category not in state_dict:
            state_dict[category] = {}
            state_dict[category]["pkg.installed"] = [{}]
            state_dict[category]["pkg.installed"][0]["pkgs"] = []

        for software in software_list.all():
            state_dict[category]["pkg.installed"][0]["pkgs"].append({software.name : software.version})

    def create_yaml(self, path, data_dict):
        with open(path, 'w') as outfile:
            yaml.dump(data_dict, outfile, default_flow_style=False)
