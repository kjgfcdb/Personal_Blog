from datetime import datetime, timezone

from django.template.defaultfilters import register


@register.filter('dateformat')
def dateformat(t):
    try:
        return datetime.fromtimestamp(t). \
            replace(tzinfo=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return t.__format__('%Y-%m-%d %H:%M:%S')


@register.filter('br')
def br(s):
    # Convert the '\n' to '<br>'
    return s.replace('\n', '<br>')
