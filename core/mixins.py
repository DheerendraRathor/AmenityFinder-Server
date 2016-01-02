

class SerializerClassRequestContextMixin(object):

    def get_context_serializer_class(self, klass, instance, **kwargs):
        context = self.get_serializer_context()
        supplied_context = kwargs.pop('context', {})
        context.update(supplied_context)
        return klass(instance, context=context, **kwargs)