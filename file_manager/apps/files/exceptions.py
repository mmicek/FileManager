from apps.common.exceptions import CustomApiException


class IncorrectMediaFileException(CustomApiException):
    default_detail = "Please upload a valid media file."
    error_code = 410001


class FileAlreadyExistsException(CustomApiException):
    default_detail = "File already exists. Use overwrite=true to replace."
    error_code = 410002
