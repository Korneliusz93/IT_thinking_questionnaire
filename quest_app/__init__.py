from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.add_jinja2_search_path('quest_app:templates')
        config.include('.routes')
        config.add_route('success_page', '/success')
        config.add_route('submit', '/submit')
        config.add_static_view('deform_static', 'deform:static/')
        config.scan()
    return config.make_wsgi_app()
