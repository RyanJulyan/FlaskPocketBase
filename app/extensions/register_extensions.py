import os
import importlib

from app.extensions.get_enabled_extensions import get_enabled_extensions

DEFAULT_EXTENSIONS_DIRECTORY = 'app/extensions/'


def list_folders(directory):
  return [
    d for d in os.listdir(directory)
    if os.path.isdir(os.path.join(directory, d))
  ]


def register_extensions(
    app, extensions_directory: str = DEFAULT_EXTENSIONS_DIRECTORY):

  @app.before_request
  def before_request():
    enabled_extensions = get_enabled_extensions(
    )  # Get the list of enabled extensions from your database or config file

    all_extensions = list_folders(extensions_directory)

    for extension in all_extensions:
      if extension in enabled_extensions and extension not in app.blueprints:
        # The extension is enabled and not currently registered, so register it
        blueprint = importlib.import_module(f'.extensions.{extension}.views',
                                            'app').blueprint
        app.register_blueprint(blueprint)
      elif extension not in enabled_extensions and extension in app.blueprints:
        # The extension is disabled and currently registered, so unregister it
        app.blueprints.pop(extension)
