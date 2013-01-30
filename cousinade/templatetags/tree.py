from django import template


register = template.Library()

f = lambda x: {'objects': x}
register.inclusion_tag('templatetags/tree.html', name='tree')(f)
