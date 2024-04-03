from abc import ABC, abstractmethod
import os
from threading import local

from flask import current_app
from flask_admin import BaseView
from jinja2 import ChoiceLoader, FileSystemLoader

_thread_locals = local()


# Define the custom metaclass
class DynamicTemplateMeta(type(BaseView), type(ABC)):
    pass


# Use the custom metaclass to resolve the conflict
class DynamicTemplateView(BaseView, ABC, metaclass=DynamicTemplateMeta):
    @abstractmethod
    def index(self):
        pass

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def edit(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    def render(self, template, **kwargs):
        # Dynamically set the template loader based on the current view
        view_directory = os.path.dirname(os.path.abspath(__file__))
        custom_loader = FileSystemLoader(view_directory)

        # Check for an original loader stored in thread-local storage
        if not hasattr(_thread_locals, "original_loader"):
            _thread_locals.original_loader = current_app.jinja_loader

        # Temporarily override the app's loader
        current_app.jinja_loader = ChoiceLoader(
            [custom_loader, _thread_locals.original_loader]
        )

        try:
            # Render the template with the temporarily overridden loader
            rendered_template = super(DynamicTemplateView, self).render(
                template, **kwargs
            )
        finally:
            # Ensure the original loader is restored
            current_app.jinja_loader = _thread_locals.original_loader

        return rendered_template
