class ReadOnlyAdminMixin(object):
    """Disables all editing capabilities."""

    # change_form_template = "admin/view.html"

    def get_actions(self, request):
        actions = super(ReadOnlyAdminMixin, self).get_actions(request)
        del actions["delete_selected"]
        return actions

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        pass

    def delete_model(self, request, obj):
        pass

    def save_related(self, request, form, formsets, change):
        pass
