import json
import os
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

import colander
import deform.widget

import logging
log = logging.getLogger(__name__)

class QuestionnairePage(colander.MappingSchema):
    technical_blogs = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(['YES', 'NO']),
        widget=deform.widget.RadioChoiceWidget(values=[('YES', 'Yes'), ('NO', 'No')])
    )
    programming_changes_thinking = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(['YES', 'NO']),
        widget=deform.widget.RadioChoiceWidget(values=[('YES', 'Yes'), ('NO', 'No')])
    )
    programming_changes_detail = colander.SchemaNode(
        colander.String(),
        missing='',  # Optional
        widget=deform.widget.TextAreaWidget()
    )
    coding_art_tool = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(['ART', 'TOOL']),
        widget=deform.widget.RadioChoiceWidget(values=[('ART', 'Art'), ('TOOL', 'Tool')])
    )
    machines_replace_creativity = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(['YES', 'NO']),
        widget=deform.widget.RadioChoiceWidget(values=[('YES', 'Yes'), ('NO', 'No')])
    )
    convey_values = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(['YES', 'NO']),
        widget=deform.widget.RadioChoiceWidget(values=[('YES', 'Yes'), ('NO', 'No')])
    )
    convey_values_detail = colander.SchemaNode(
        colander.String(),
        missing='',
        widget=deform.widget.TextAreaWidget()
    )
    technology_unite_divide = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(['BRINGS_TOGETHER', 'DIVIDES']),
        widget=deform.widget.RadioChoiceWidget(values=[('BRINGS_TOGETHER', 'Brings together'), ('DIVIDES', 'Divides')])
    )
    ethical_challenges = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(['YES', 'NO']),
        widget=deform.widget.RadioChoiceWidget(values=[('YES', 'Yes'), ('NO', 'No')])
    )
    ethical_challenges_detail = colander.SchemaNode(
        colander.String(),
        missing='',
        widget=deform.widget.TextAreaWidget()
    )
    worth_sharing_knowledge = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(['YES', 'NO']),
        widget=deform.widget.RadioChoiceWidget(values=[('YES', 'Yes'), ('NO', 'No')])
    )
    define_success = colander.SchemaNode(
        colander.String(),
        missing='',
        widget=deform.widget.TextAreaWidget()
    )
    role_of_ai = colander.SchemaNode(
        colander.String(),
        missing='',
        widget=deform.widget.TextAreaWidget()
    )
    work_influence_society = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(['YES', 'NO']),
        widget=deform.widget.RadioChoiceWidget(values=[('YES', 'Yes'), ('NO', 'No')])
    )
    social_media_support = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(['YES', 'NO']),
        widget=deform.widget.RadioChoiceWidget(values=[('YES', 'Yes'), ('NO', 'No')])
    )
    responsible_social_impact = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(['YES', 'NO']),
        widget=deform.widget.RadioChoiceWidget(values=[('YES', 'Yes'), ('NO', 'No')])
    )
    importance_engage_wider = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(['YES', 'NO']),
        widget=deform.widget.RadioChoiceWidget(values=[('YES', 'Yes'), ('NO', 'No')])
    )
    online_participation_changed = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(['YES', 'NO']),
        widget=deform.widget.RadioChoiceWidget(values=[('YES', 'Yes'), ('NO', 'No')])
    )




@view_config(route_name='home', renderer='/templates/questionnaire.jinja2')
def questionnaire_fill(request):
    schema = QuestionnairePage()
    form = deform.Form(schema)


    if 'submit' in request.params:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
        except deform.ValidationFailure as e:
            return {'form': e.render()}

        json_path = os.path.join(os.path.dirname(__file__), 'responses.json')


        # Load existing responses
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                try:
                    all_responses = json.load(f)
                except json.JSONDecodeError:
                    all_responses = []
        else:
            all_responses = []

        # Append the new response
        all_responses.append(appstruct)

        # Save updated responses
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(all_responses, f, ensure_ascii=False, indent=4)

        # Redirect after submission
        return HTTPFound(request.route_url('success_page'))

    return {'form': form.render()}

@view_config(route_name='success_page', renderer='success.jinja2')
def success_page(request):
    return {'message': 'Your response has been recorded successfully!'}