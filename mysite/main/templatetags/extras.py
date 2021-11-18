from django import template

register = template.Library()

@register.filter
def in_category(things, category):
    return things.filter(type=category)

@register.filter
def in_category_count(things, category):
    return len(things.filter(type=category))

@register.filter
def in_stalker(things, category):
    return things.filter(stalker=category)

@register.filter
def multiply(things, count):
    return things * count

@register.filter
def in_stalker_count(things, category):
    return len(things.filter(stalker=category))

@register.filter
def in_user_article_count(things, category):
    return len(things.filter(author=category))