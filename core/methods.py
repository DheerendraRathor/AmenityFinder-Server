"""
Contains core methods which will be used project-wide
"""
import uuid


def file_uploader(filename, instance):
    """
    Return UUID generated filename
    :type filename: str
    """
    generated_filename = uuid.uuid4().hex
    uploaded_extension = filename.split('.')
    if len(uploaded_extension) > 0:
        extension = uploaded_extension[-1]
    else:
        extension = 'png'
    return "%s.%s" % (generated_filename, extension)
