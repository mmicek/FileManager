import filetype
from apps.common.enums import MediaType
from apps.files.exceptions import IncorrectMediaFileException


class MediaTypeValidator:
    POSSIBLE_MEDIA_TYPES = list(MediaType)

    def __init__(self, supported_media_types):
        if not set(supported_media_types).issubset(self.POSSIBLE_MEDIA_TYPES):
            raise ValueError(
                f"Configuration error: supported_media_types list includes illegal file types. "
                f"Possible types: {self.POSSIBLE_MEDIA_TYPES}"
            )
        self.supported_media_types = supported_media_types

    def __call__(self, value):
        file = value.file
        file_extension = filetype.guess_extension(file)
        if file_extension not in self.supported_media_types:
            raise IncorrectMediaFileException(extra={"supported_types": "".join(self.supported_media_types)})
