from .base import TamperBase
from .randomcase import RandomCase
from .space2comment import Space2Comment
from .charencode import CharEncode
from .between import Between
from .apostrophemask import ApostropheMask
from .space2plus import Space2Plus
from .charunicodeencode import CharUnicodeEncode

tampers = {
    'randomcase': RandomCase,
    'space2comment': Space2Comment,
    'charencode': CharEncode,
    'between': Between,
    'apostrophemask': ApostropheMask,
    'space2plus': Space2Plus,
    'charunicodeencode': CharUnicodeEncode
}