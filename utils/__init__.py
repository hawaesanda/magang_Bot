# Utils package - modular screenshot functions for Looker Studio dashboards

from .base import init_browser, crop_image
from .router import get_looker_studio_screenshot
from .helpers import send_report_with_loading_cleanup

# Import specialized screenshot functions
from .assurance import (
    take_monitoring_ticket_screenshot,
    take_closed_ticket_screenshot,
    take_unspec_screenshot
)

from .provisioning import (
    take_funneling_screenshot,
    take_detail_kendala_psb_screenshot,
    take_detail_wo_screenshot
)

from .indbiz import (
    take_funneling_indbiz_screenshot,
    take_detail_kendala_indbiz_screenshot,
    take_detail_wo_indbiz_screenshot
)

from .b2b import (
    take_monitoring_ticket_b2b_screenshot,
    take_performance_b2b_screenshot
)

from .imjas import take_imjas_screenshot
from .sections import get_section_screenshot, get_screenshot_by_element
from .reports import take_msawsa_screenshot, take_pilaten_screenshot

# Make all functions available at package level
__all__ = [
    # Base functions
    'init_browser',
    'crop_image',
    'get_looker_studio_screenshot',
    'send_report_with_loading_cleanup',
    
    # Assurance functions
    'take_monitoring_ticket_screenshot',
    'take_closed_ticket_screenshot',
    'take_unspec_screenshot',
    
    # Provisioning functions
    'take_funneling_screenshot',
    'take_detail_kendala_psb_screenshot',
    'take_detail_wo_screenshot',
    
    # INDBIZ functions
    'take_funneling_indbiz_screenshot',
    'take_detail_kendala_indbiz_screenshot',
    'take_detail_wo_indbiz_screenshot',
    
    # B2B functions
    'take_monitoring_ticket_b2b_screenshot',
    'take_performance_b2b_screenshot',
    
    # IMJAS functions
    'take_imjas_screenshot',
    
    # Section functions
    'get_section_screenshot',
    'get_screenshot_by_element',
    
    # Reports functions
    'take_msawsa_screenshot',
    'take_pilaten_screenshot',
]
