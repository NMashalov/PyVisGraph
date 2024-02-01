print('Well it runs')
from pyvisgraph import register

@register(
    inputs=[('Hello','CS_NODE_MODELS')]
)
def hello(n: str):
    return n

@register()
def bye(no):
    return no