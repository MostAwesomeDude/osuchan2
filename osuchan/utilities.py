import hashlib
import mimetypes

def chan_filename(f):
    """
    Given an uploaded file, determine a filename for it.

    The filenames produced by this function are always reasonable and secure.
    """

    hash = hashlib.md5(f.stream.read())
    f.stream.seek(0)

    md5sum = hash.hexdigest()

    extension = mimetypes.guess_extension(f.content_type)

    return "%s%s" % (md5sum, extension)
