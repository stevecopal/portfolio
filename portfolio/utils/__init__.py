# portfolio/utils/__init__.py

# Context Processors
from .context_processors import global_context, seo_context

# SEO
from .seo import (
    get_seo_meta,
    get_open_graph_meta,
    get_canonical_url,
    get_structured_data,
)

# Helpers
from .helpers import (
    generate_slug,
    format_date,
    truncate_text,
    get_absolute_url,
    get_model_name,
    get_reading_time,
    get_client_ip,
    get_user_agent,
    is_mobile,
    is_ajax,
    get_next_url,
    validate_email,
    validate_phone,
    sanitize_html,
    get_pagination_range,
)

__all__ = [
    # Context Processors
    "global_context",
    "seo_context",
    # SEO
    "get_seo_meta",
    "get_open_graph_meta",
    "get_canonical_url",
    "get_structured_data",
    # Helpers
    "generate_slug",
    "format_date",
    "truncate_text",
    "get_absolute_url",
    "get_model_name",
    "get_reading_time",
    "get_client_ip",
    "get_user_agent",
    "is_mobile",
    "is_ajax",
    "get_next_url",
    "validate_email",
    "validate_phone",
    "sanitize_html",
    "get_pagination_range",
]