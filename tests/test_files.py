from tempfile import NamedTemporaryFile

import pytest
from pydantic import ConfigDict
from testapp.models import Attachment

from djantic import ModelSchema


@pytest.mark.django_db
def test_image_field_schema():
    class AttachmentSchema(ModelSchema):
        model_config = ConfigDict(model=Attachment)

    image_file = NamedTemporaryFile(suffix=".jpg")
    attachment = Attachment.objects.create(
        description="My image upload",
        image=image_file.name,
    )

    assert AttachmentSchema.model_json_schema() == {
        "description": "Attachment(id, description, image)",
        "properties": {
            "id": {
                "anyOf": [{"type": "integer"}, {"type": "null"}],
                "default": None,
                "description": "id",
                "title": "Id",
            },
            "description": {
                "description": "description",
                "maxLength": 255,
                "title": "Description",
                "type": "string",
            },
            "image": {
                "anyOf": [{"maxLength": 100, "type": "string"}, {"type": "null"}],
                "default": None,
                "description": "image",
                "title": "Image",
            },
        },
        "required": ["description"],
        "title": "AttachmentSchema",
        "type": "object",
    }

    assert AttachmentSchema.from_django(attachment).dict() == {
        "id": attachment.id,
        "description": attachment.description,
        "image": attachment.image.name,
    }


@pytest.mark.django_db
def test_model_validate():
    class AttachmentSchema(ModelSchema):
        model_config = ConfigDict(model=Attachment)

    image_file = NamedTemporaryFile(suffix=".jpg")
    attachment = Attachment.objects.create(
        description="My image upload",
        image=image_file.name,
    )
    raw_init_item = AttachmentSchema.model_validate(
        attachment,
        from_attributes=True,
    )

    wrapper_item = AttachmentSchema.from_django(attachment)
    assert wrapper_item == raw_init_item
