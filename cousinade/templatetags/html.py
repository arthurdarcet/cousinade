from django import template


register = template.Library()

MIME_TYPES = {
    'less': 'less',
    'js': 'javascript',
}

def do(*args):
    ret = []
    for path in args:
        extension = path.rsplit('.',1)[1]
        mime = MIME_TYPES.get(extension, extension)
        ret.append({'path': path, 'extension': extension, 'mime': mime})
    return {'l': ret}

register.inclusion_tag('templatetags/css.html', name='css')(do)
register.inclusion_tag('templatetags/js.html', name='js')(do)
