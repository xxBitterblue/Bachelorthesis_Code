from django.shortcuts import get_list_or_404, get_object_or_404
from validation.models import ValidationRule, ValidationRuleDto
from core_application.models import Category
from software.models import ImmutableSoftware, Software
from django.http import Http404


class ValidationService:

    def get_all(self):
        return get_list_or_404(ValidationRule)

    def get_rule(self, id):
        return get_object_or_404(ValidationRule, pk=id)

    def add_rule(self, name, active, is_global, rule, categorys, author):
        validation_rule = ValidationRule(name=name, active=active, is_global=is_global, rule=rule, author=author)
        validation_rule.save()

        if not is_global:
            self.fill_categorys(validation_rule, categorys)

        return validation_rule

    def delete(self, id):
        validation_rule = get_object_or_404(ValidationRule, pk=id)
        validation_rule.delete()
        return True

    def update(self, id, name, active, is_global, rule, categorys):
        validation_rule = get_object_or_404(ValidationRule, pk=id)
        validation_rule.name = name
        validation_rule.active = active
        validation_rule.is_global = is_global
        validation_rule.rule = rule
        validation_rule.save()

        validation_rule.categorys.clear()

        if not validation_rule.is_global:
            self.fill_categorys(validation_rule, categorys)

        return validation_rule

    def get_validation_structure(self):
        test_software1 = Software(name="example", version="1.0", type="software_type")
        test_software2 = Software(name="example", version="1.1", type="software_type")
        validation_exceptions = ["ValidationRuleException", "ValidationRuleVersionException"]

        return [test_software1, test_software2], validation_exceptions

    def validate_group(self, software_list, category):
        category_exists = False
        if bool(category):
            category = Category.objects.filter(pk=category["category_id"])
            category_exists = True
        all_validation_rules = ValidationRuleDto.objects.filter(active=True)
        software_list = [get_object_or_404(ImmutableSoftware, pk=software["software_id"]) for software in software_list]

        for rule in all_validation_rules:
            if rule.is_global or category_exists and category in rule.categorys.all():
                rule.validate(software_list)

    def fill_categorys(self, validation_rule, categorys):
        for curr_category in categorys:
            id = curr_category["category_id"]
            try:
                category = get_object_or_404(Category, pk=id)
                validation_rule.categorys.add(category)
            except Category.DoesNotExist:
                raise Http404("Category could not be found with id:" + str(id))
