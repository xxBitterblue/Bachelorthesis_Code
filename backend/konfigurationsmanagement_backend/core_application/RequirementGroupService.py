import datetime
import json
from django.http import Http404
from core_application.models import Setting, Category, RequirementGroup, CategoryRequirementGroup,UserComment, ChangeHistoryEntry
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.models import User
from authentication.models import DashboardEntry
from software.models import Software
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class RequirementGroupService:
    def __init__(self):
        self.layer = get_channel_layer()

    def get_requirement_groups(self):
        return get_list_or_404(RequirementGroup)

    def get_requirement_group(self, id):
        return get_object_or_404(RequirementGroup, pk=id)

    def get_groups_by_category(self, category_id):
        category = get_object_or_404(Category, pk=category_id)
        all_requirement_groups = RequirementGroup.objects.filter(category=category)
        all_category_groups = CategoryRequirementGroup.objects.filter(category=category)
        return all_requirement_groups, all_category_groups

    def add_requirement_group(self, name, status, status_comment, author, category, software_list):
        category_object = get_object_or_404(Category, pk=category["category_id"])
        if not self.check_deadline(category_object):
            return None
        current_time = datetime.datetime.now().date()
        comment = status_comment if status_comment != "" else None
        requirement_group = RequirementGroup(requirement_group_name=name, status=status, status_comment=comment, author=author, timestamp=current_time, category=category_object)
        requirement_group.save()

        self.fill_software(requirement_group, software_list)

        return requirement_group

    def update_requirement_group(self, id, name, status, status_comment, author, category, software_list, change_reason):
        requirement_group = get_object_or_404(RequirementGroup, pk=id)
        category_object = get_object_or_404(Category, pk=category["category_id"])
        changes = {}

        if not self.check_deadline(category_object):
            return None

        self.update_helper(requirement_group, changes, category_object, name, status, status_comment, software_list)

        self.add_change_histry_entry(requirement_group, author, json.dumps(changes), change_reason)

        return requirement_group

    def delete_requirement_group(self, id):
        requirement_group = get_object_or_404(RequirementGroup, pk=id)
        requirement_group.delete()
        return True

    def get_category_requirement_groups(self):
        return get_list_or_404(CategoryRequirementGroup)

    def get_category_requirement_group(self, id):
        return get_object_or_404(CategoryRequirementGroup, pk=id)

    def add_category_requirement_group(self, name, status, status_comment, author, category, software_list, reference_groups):
        current_time = datetime.datetime.now().date()
        comment = status_comment if status_comment != "" else None
        category_object = get_object_or_404(Category, pk=category["category_id"])
        if not self.check_deadline(category_object):
            return None
        category_requirement_group = CategoryRequirementGroup(requirement_group_name=name, status=status, status_comment=comment, author=author, timestamp=current_time, category=category_object)
        category_requirement_group.save()

        self.fill_software(category_requirement_group, software_list)
        self.fill_reference_groups(category_requirement_group, reference_groups)

        return category_requirement_group

    def update_category_requirement_group(self, id, requirement_group_name, status, status_comment, author, category, software_list, change_reason, reference_groups):
        category_group = get_object_or_404(CategoryRequirementGroup, pk=id)
        category_object = get_object_or_404(Category, pk=category["category_id"])
        changes = {}

        if not self.check_deadline(category_object):
            return None

        self.update_helper(category_group, changes, category_object, requirement_group_name, status, status_comment, software_list)

        old_reference_list = [reference for reference in category_group.reference_groups.all()]

        category_group.reference_groups.clear()
        self.fill_reference_groups(category_group, reference_groups)

        new_reference_list = [reference for reference in category_group.reference_groups.all()]

        reference_both_list = set.intersection(set(new_reference_list), set(old_reference_list))
        deleted_reference_list = list(set(old_reference_list) - reference_both_list)
        new_added_list = list(set(new_reference_list) - reference_both_list)

        if len(deleted_reference_list) != 0 or len(new_added_list) != 0:
            changes["reference_list"] = {}
            changes["reference_list"]["deleted_references"] = deleted_reference_list
            changes["reference_list"]["added_references"] = new_added_list

        self.add_change_histry_entry(category_group, author, json.dumps(changes), change_reason)

        return category_group

    def delete_category_requirement_group(self, id):
        category_group = get_object_or_404(CategoryRequirementGroup, pk=id)
        category_group.delete()
        return True

    def add_change_histry_entry(self, requirement_group, author, changes, change_reason):
        reason = change_reason if change_reason != "" else None
        current_time = datetime.datetime.now()
        change_history_entry = ChangeHistoryEntry(author=author, changes=changes, change_reason=reason, timestamp=current_time)
        change_history_entry.save()
        requirement_group.change_history.add(change_history_entry)

    def add_user_comment(self, id, author, comment_text):
        current_time = datetime.datetime.now()
        requirement_group = get_object_or_404(RequirementGroup, pk=id)
        user_comment = UserComment(author=author, comment_text=comment_text, timestamp=current_time)
        user_comment.save()

        requirement_group.user_comments.add(user_comment)

        involved_users = [user for user in self.get_involved_users(requirement_group) if user.id is not author.id]

        for user in involved_users:
            new_entry = self.create_dashboard_entry(requirement_group.id, 'Neuer Kommentar wurde hinzugefuegt', author)
            user.additionaluserinformation.dashboard.add(new_entry)
            self.send_socket_msg(user.id, 'new_changes', new_entry.as_json_without_time())

        return True

    def get_all_settings(self):
        return get_list_or_404(Setting)

    def add_setting(self, deadline, author, required_users, categorys):
        setting = Setting(deadline=deadline, author=author)
        setting.save()

        if len(required_users) > 0:
            self.fill_required_users(setting, required_users)

        self.fill_categorys(setting, categorys)
        return setting

    def delete_setting(self, id):
        setting = get_object_or_404(Setting, pk=id)
        setting.delete()
        return True

    def get_all_categorys(self):
        return get_list_or_404(Category)

    def get_required_users(self, id):
        category = get_object_or_404(Category, pk=id)
        setting_list = Setting.objects.filter(categorys__in=[category])
        required_users = []

        for setting in setting_list:
            required_users.extend(setting.required_users.all())

        return required_users

    def add_category(self, category_name, parent):
        parent_category = get_object_or_404(Category, pk=parent["category_id"])
        category = Category(category_name=category_name, parent=parent_category)
        category.save()

        return category

    def get_dashboard(self, user_id):
        user = get_object_or_404(User, pk=user_id)
        return user.additionaluserinformation.dashboard

    def fill_required_users(self, setting, required_users):
        for curr_user in required_users:
            id = curr_user["user_id"]
            try:
                required_user = User.objects.get(pk=id)
                setting.required_users.add(required_user)
            except User.DoesNotExist:
                raise Http404("User could not be found with id:" + str(id))

    def fill_categorys(self, setting, categorys):
        for curr_category in categorys:
            id = curr_category["category_id"]
            try:
                category = get_object_or_404(Category, pk=id)
                setting.categorys.add(category)
            except Category.DoesNotExist:
                raise Http404("Category could not be found with id:" + str(id))

    def fill_software(self, requirement_group, software_list):
        for software in software_list:
            id = software["software_id"]
            try:
                software = get_object_or_404(Software, pk=id)
                requirement_group.software_list.add(software)
            except Software.DoesNotExist:
                raise Http404("Software could not be found with id:" + str(id))

    def fill_reference_groups(self, category_group, requirement_groups):
        for id in requirement_groups:
            try:
                group = get_object_or_404(RequirementGroup, pk=id)
                category_group.reference_groups.add(group)
            except RequirementGroup.DoesNotExist:
                raise Http404("RequirementGroup could not be found with id:" + str(id))

    def update_helper(self, group, changes, category, name, status, status_comment, software_list):
        if category != group.category:
            changes["category"] = {}
            changes["category"]["previous"] = group.category.as_json()
            changes["category"]["now"] = category.as_json()
            group.category = category

        if name != group.requirement_group_name:
            changes["requirement_group"] = {}
            changes["requirement_group"]["previous"] = group.requirement_group_name
            changes["requirement_group"]["now"] = name
            group.requirement_group_name = name

        if status != group.status:
            changes["status"] = {}
            changes["status"]["previous"] = group.status
            changes["status"]["now"] = status
            group.status = status

        if status_comment != group.status_comment:
            changes["status_comment"] = {}
            changes["status_comment"]["previous"] = "" if group.status_comment is None else group.status_comment
            changes["status_comment"]["now"] = "" if status_comment is None else status_comment
            group.status_comment = status_comment

        group.save()
        old_software_list = [software for software in group.software_list.all()]

        group.software_list.clear()
        self.fill_software(group, software_list)

        new_software_list = [software for software in group.software_list.all()]

        software_in_both_lists = set.intersection(set(new_software_list), set(old_software_list))
        deleted_software_list = list(set(old_software_list) - software_in_both_lists)
        new_added_list = list(set(new_software_list) - software_in_both_lists)

        if len(deleted_software_list) != 0 or len(new_added_list) != 0:
            changes["software_list"] = {}
            changes["software_list"]["deleted_software"] = [software.as_json() for software in deleted_software_list]
            changes["software_list"]["added_software"] = [software.as_json() for software in new_added_list]

    def create_dashboard_entry(self, group_id, message, editor):
        current_time = datetime.datetime.now().date()

        new_entry = DashboardEntry(type_id=group_id, message=message, timestamp=current_time, editor=editor)
        new_entry.save()

        return new_entry

    def get_involved_users(self, requirement_group):
        comment_users = [comment.author for comment in requirement_group.user_comments.all()]
        comment_users.append(requirement_group.author)
        editor = [history_entry.author for history_entry in requirement_group.change_history.all()]

        users = list(set(comment_users + editor))

        return users

    def send_socket_msg(self, user_id, event_type, content):
        async_to_sync(self.layer.group_send)(f'user_{user_id}', {
            'type': event_type,
            'content': content
        })

    def check_deadline(self, category):
        current_time = datetime.datetime.now().date()
        settings = Setting.objects.filter(categorys__in=[category])

        for setting in settings:
            if setting.deadline <= current_time:
                return False

        return True
