from django import template

register = template.Library() # template에 있는 Library를 register에 담아놓겠다

# @ : annotation(백엔드에서 주석과 같이 사용. 시스템이 읽는 주석)
# 애너테이션을 적용하면 템플릿에서 함수를 적용할 수 있게 된다
@register.filter
def sub(value, arg): # 사용자 정의 함수
    return value - arg
