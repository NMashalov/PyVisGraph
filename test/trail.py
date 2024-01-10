from pydantic import (
    create_model,
    BaseModel
)

class SettingsClass(BaseModel):
    name: str

def _register_new_model():
    global SettingsClass
    SettingsClass = create_model(
        'DynamicFoobarModel', timetable = (str,...)
    )

print(SettingsClass(name='nikita'))
_register_new_model()
print(SettingsClass(name='nikita'))
