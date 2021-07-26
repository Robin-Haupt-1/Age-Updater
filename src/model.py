"""
Manages note type and templates
"""
from .constants import *
from .utils import *

def add_model(col):
    """Add 'Age Updater Note' note type to collection"""
    models = col.models
    model = models.new(NOTETYPE_NAME)
    model['type'] = 0  # default model type

    for f in FIELD_NAMES:
        field = models.newField(f)
        models.addField(model, field)

    template = models.newTemplate("1")
    template['qfmt'] = CARD_FRONT
    template['afmt'] = CARD_BACK
    model['css'] = CARD_CSS
    model['sortf'] = 0  # set sort field to 'Name'
    models.addTemplate(model, template)
    models.add(model)




def check_model(col):
    models = col.models
    existing_model = models.byName(NOTETYPE_NAME)
    if not existing_model:
        add_model(col)
        return True
    existing_model_fields = [f['name'] for f in existing_model['flds']]
    all_fields_exist = True
    for field_name in FIELD_NAMES:
        if field_name not in existing_model_fields:
            all_fields_exist = False
            break

    if not all_fields_exist:
        display_warning('Your "Age Updater Note" note type is not set up properly. '
                       "Please make sure that it includes all of the following fields: <br><br>- "
                       f"<i>{'<br>- '.join(FIELD_NAMES)}</i><br>")
    return all_fields_exist
