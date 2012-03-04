from django.test import TestCase
from django.template import Context, Template


class TestMenuTemplateTag(TestCase):

    def should_make_a_menu_link_as_active(self):
        html = "{% is_active request.get_full_path 'home' %}"
        template = Template(html)
        context = Context({'request': {"get_full_path": "home"}})

        self.assertEqual("active", template.render(context))

    # def should_make_a_menu_link_as_not_active(self):
    #     html = "{% is_active request.get_full_path 'home' %}"
    #     template = Template(html)
    #     context = Context({'request': {"get_full_path": "register"}})

    #     self.assertNotEqual("", template.render(context))
