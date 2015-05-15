class PlainObject(object):

    def __init__(self, **kwargs):

        for attr in ('__attrs__', '__attrs_required__'):
            if not hasattr(self, attr):
                raise NotImplementedError(attr + ' attribute is required.')

        for attr in self.__attrs__:
            value = kwargs.get(attr, None)

            if value is None and attr in self.__attrs_required__:
                raise ValueError('%s.%s: value is required.' %
                                 (self.__class__.__name__, attr))

            setattr(self, '_%s' % attr, value)

    def _fetch_field(self, attr):
        # Default behaviour: return the underlying attribute value.
        return getattr(self, '_%s' % attr, None)


class VKObject(PlainObject):

    def __init__(self, **kwargs):

        if '__vk__' not in kwargs:
            raise ValueError('%s: VK handler is required.'
                             % self.__class__.__name__)

        self._vk = kwargs['__vk__']
        super(VKObject, self).__init__(**kwargs)
