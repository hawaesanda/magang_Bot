# Import all handlers from different modules
from .base import start, test_scheduler
from .reports import msawsa, pilaten
from .assurance import monitoring, closed_ticket, unspec
from .provisioning import funneling, detail_kendala_psb, detail_wo
from .indbiz import funneling_indbiz, detail_kendala_indbiz, detail_wo_indbiz
from .b2b import monitoring_ticket_b2b, performance
from .imjas import im3as

# Make all handlers available when importing from handlers package
__all__ = [
    'start', 'test_scheduler',
    'msawsa', 'pilaten',
    'monitoring', 'closed_ticket', 'unspec',
    'funneling', 'detail_kendala_psb', 'detail_wo',
    'funneling_indbiz', 'detail_kendala_indbiz', 'detail_wo_indbiz',
    'monitoring_ticket_b2b', 'performance',
    'imjas'
]
