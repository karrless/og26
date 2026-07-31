from . import menu, form, faq

routers = [form.router, faq.router, menu.router, menu.default_router]