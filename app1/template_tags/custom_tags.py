from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    print(dictionary)
    try:
        y=dictionary.get(key)
    except:
        y=[]
        
    return y