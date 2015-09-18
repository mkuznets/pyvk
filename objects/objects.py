from . import base


class User(base.User):

    def _fetch_fields(self, *fields):

        if set(fields) - set(self.__attrs__):
            raise IndexError('Nonexistent fields: %s' % fields)

        r = self._vk.req('users.get', {'user_ids': self.id,
                                   'fields': ','.join(fields)})
        user = r['response'][0]

        for field in fields:
            setattr(self, field, user[field])

    def get_friends(self):
        pass
