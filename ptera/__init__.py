from .categories import Category, cat  # noqa
from .core import (  # noqa
    PatternCollection,
    PteraFunction,
    interact,
    overlay,
    to_pattern,
)
from .recur import Recurrence  # noqa
from .selfless import (  # noqa
    ConflictError,
    Override,
    default,
    override,
    transform,
)
from .storage import Storage, initializer, updater, valuer  # noqa
from .tools import Configurator, auto_cli, catalogue  # noqa


class PteraDecorator:
    def __init__(self, kwargs):
        self.kwargs = kwargs

    def defaults(self, **defaults):
        return self({**self.kwargs, "defaults": defaults})

    def __call__(self, fn):
        new_fn, state = transform(fn, interact=interact)
        fn = PteraFunction(new_fn, state)
        if "defaults" in self.kwargs:
            fn = fn.new(**self.kwargs)
        return fn


ptera = PteraDecorator({})
