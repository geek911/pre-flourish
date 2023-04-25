from django.conf import settings
from edc_model_wrapper import ModelWrapper

from .child_assent_model_wrapper_mixin import ChildAssentModelWrapperMixin

from .child_dummy_consent_model_wrapper_mixin import \
    ChildDummyConsentModelWrapperMixin



class ChildDummyConsentModelWrapper(ChildDummyConsentModelWrapperMixin,
                                    ChildAssentModelWrapperMixin,
                                    ModelWrapper):
    model = 'pre_flourish.preflourishchilddummysubjectconsent'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'pre_flourish_child_listboard_url')
    next_url_attrs = ['subject_identifier', 'screening_identifier']
    querystring_attrs = ['subject_identifier', 'screening_identifier']
