from schematics.models import Model
from schematics.exceptions import (
        ConversionError,
        ModelValidationError,
        ValidationError,
)

from ...constants import *
from ...exceptions import ActionFieldError
from ...logger import create_logger


class Action(Model):
    """A single action/endpoint for a service.

    An Action is invoked in an rpc-style mechanism, where the service will instantiate an Action
    instance and execute it via the ``execute_run`` method.

    """
    @classmethod
    def get_instance(action_klass, raw_data=None, deserialize_mapping=None, strict=True,
            **rpc_kwargs):
        """Entry point into the Action, invoked by the service."""
        rpc_kwargs = action_klass.pre_run(**rpc_kwargs)

        try:
            return action_klass(raw_data=rpc_kwargs,
                        deserialize_mapping=deserialize_mapping, strict=strict)
        except ConversionError, err:
            raise ActionFieldError(err)

    @classmethod
    def pre_run(klass, **kwargs):
        """Hook before ``run`` is called.

        Should return the kwargs passed to Action contructor.  Note this is just for the
        constructor of the ``Action``, not for the actual ``run method.
        """
        return kwargs

    @property
    def logger(self):
        self._logger = getattr(self, '_logger', None)
        if self._logger and self._logger.name == self.logger_name:
            return self._logger

        self._logger = create_logger(self.__class__.__name__)
        return self._logger

    def execute_run(self, service):
        """Actually execute the action by doing any setup/bootstrap and calling ``run``.

        After instantiation, fields will have been transformed and computed based on rpc_kwargs
        inputs.  The rpc_kwargs/action_args are fields passed to the service as kwargs::

            results = client.do_some_action(name='bz', age=29)

        """
        self._errors = []

        # validate input arguments
        if self.is_valid():
            action_kwargs = self.get_action_kwargs()
            self.run(**action_kwargs)

        # revalidate since the run method could have attached some new
        # attributes.
        #
        # TODO - There may be a better way to handle this since the service itself shouldn't be
        # creating any internal validation errors/issues.
        #
        try:
            self.validate()
            final_results = self.finalize_results()
        except ModelValidationError, err:
            raise ActionFieldError(err)

        return final_results

    def get_action_kwargs(self):
        """Another hook which can control kwargs to the run method."""
        return {}

    def add_error(self, msg, error_type, hint=''):
        """Add an action error"""
        self._errors.append({
            'error': msg,
            'error_type': error_type,
            'hint': hint})

    def add_client_error(self, msg, hint=''):
        """Add a specific type of error indicating that the client did something wrong."""
        self.add_error(msg, CLIENT_ERROR, hint)

    def add_server_error(self, msg, hint=''):
        """Add a specific type of error indicating that the server had some sort of issue."""
        self.add_error(msg, SERVER_ERROR, hint)

    def get_errors(self):
        return self._errors

    def run(self, **kwargs):
        raise NotImplementedError('Clients must implement this method')

    def _response_names_and_fields_iter(self):
        for fieldname, field in self._fields.iteritems():
            if getattr(field, 'in_response', None):
                yield (fieldname, field)

    def finalize_results(self):
        """Grep out the final results/attributes the action should return."""
        results = {}
        for fieldname, field in self._response_names_and_fields_iter():
            value = getattr(self, fieldname)
            fieldname = field.serialized_name or fieldname
            results[fieldname] = field.to_native(value)

        return results

    def is_valid(self):
        if self._errors:
            return False

        try:
            self.validate()
            return True
        except ValidationError, err:
            self._errors = err.messages
            return False
