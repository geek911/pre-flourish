from django import template
from django.conf import settings
from edc_base.utils import age, get_utcnow

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.inclusion_tag('pre_flourish/buttons/consent_button.html')
def consent_button(model_wrapper):
    title = ['Consent subject to participate.']
    return dict(
        subject_identifier=model_wrapper.consent.object.subject_identifier,
        subject_screening_obj=model_wrapper.object,
        add_consent_href=model_wrapper.consent.href,
        # consent_version=model_wrapper.consent_version,
        title=' '.join(title))


@register.inclusion_tag('pre_flourish/buttons/dashboard_button.html')
def dashboard_button(model_wrapper):
    pre_flourish_subject_dashboard_url = settings.DASHBOARD_URL_NAMES.get(
        'pre_flourish_subject_dashboard_url')
    return dict(
        pre_flourish_subject_dashboard_url=pre_flourish_subject_dashboard_url,
        subject_identifier=model_wrapper.subject_identifier)


@register.inclusion_tag('flourish_dashboard/buttons/locator_button.html')
def locator_button(model_wrapper):
    return dict(
        add_locator_href=model_wrapper.caregiver_locator.href,
        screening_identifier=model_wrapper.object.screening_identifier,
        caregiver_locator_obj=model_wrapper.locator_model_obj)


@register.inclusion_tag('pre_flourish/buttons/edit_screening_button.html')
def edit_screening_button(model_wrapper):
    title = ['Edit Subject Screening form.']
    return dict(
        screening_identifier=model_wrapper.object.screening_identifier,
        href=model_wrapper.href,
        title=' '.join(title))


@register.inclusion_tag('pre_flourish/buttons/screening_button.html')
def screening_button(model_wrapper):
    add_screening_href = ''
    subject_screening_obj = None
    if hasattr(model_wrapper, 'maternal_screening'):
        add_screening_href = model_wrapper.maternal_screening.href
    if model_wrapper.screening_model_obj:
        subject_screening_obj = model_wrapper.screening_model_obj

    return dict(
        add_screening_href=add_screening_href,
        subject_screening_obj=subject_screening_obj
    )


@register.inclusion_tag('pre_flourish/buttons/eligibility_button.html')
def eligibility_button(model_wrapper):
    comment = []
    obj = model_wrapper.object
    tooltip = None
    if obj.ineligibility:
        comment = obj.ineligibility[1:-1].split(',')
        comment = list(set(comment))
        comment.sort()
    return dict(eligible=obj.is_eligible, comment=comment,
                tooltip=tooltip, obj=obj)


@register.inclusion_tag('pre_flourish/buttons/log_entry_button.html')
def log_entry_button(model_wrapper):
    href = model_wrapper.log_entry_model_wrapper.href
    return dict(
        href=href,
    )


@register.inclusion_tag('pre_flourish/buttons/edit_screening_button.html')
def edit_screening_button(model_wrapper):
    title = ['Edit Subject Screening form.']
    return dict(
        screening_identifier=model_wrapper.object.screening_identifier,
        href=model_wrapper.href,
        title=' '.join(title))


@register.inclusion_tag('pre_flourish/buttons/assents_button.html')
def assents_button(model_wrapper):
    title = ['Child Assent(s)']
    return dict(
        wrapped_assents=model_wrapper.wrapped_child_assents,
        child_assents_exist=model_wrapper.child_assents_exists,
        title=' '.join(title), )


@register.inclusion_tag('pre_flourish/buttons/assent_button.html')
def assent_button(model_wrapper):
    title = ['Assent child to participate.']
    return dict(
        consent_obj=model_wrapper.object,
        assent_age=model_wrapper.child_age >= 7,
        child_assent=model_wrapper.child_assent,
        title=' '.join(title))


@register.inclusion_tag(
    'flourish_dashboard/buttons/child_dashboard_button.html')
def child_dashboard_button(model_wrapper):
    child_dashboard_url = settings.DASHBOARD_URL_NAMES.get(
        'pre_flourish_child_dashboard_url')
    return dict(
        child_dashboard_url=child_dashboard_url,
        subject_identifier=model_wrapper.subject_identifier)


@register.inclusion_tag(
    'pre_flourish/buttons/caregiver_dashboard_button.html')
def caregiver_dashboard_button(model_wrapper):
    subject_dashboard_url = settings.DASHBOARD_URL_NAMES.get(
        'pre_flourish_subject_dashboard_url')

    subject_identifier = model_wrapper.object.subject_identifier

    return dict(
        subject_dashboard_url=subject_dashboard_url,
        subject_identifier=subject_identifier)


@register.simple_tag(takes_context=True)
def get_age(context, born=None):
    if born:
        reference_datetime = context.get('reference_datetime', get_utcnow())
        participant_age = age(born, reference_datetime)
        age_str = ''
        age_months = participant_age.months % 12
        if participant_age.years > 0:
            age_str += str(participant_age.years) + ' yrs '
        if age_months > 0:
            age_str += str(age_months) + ' months'
        return age_str
