from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..api import API


class BaseMixin:
    _api: API
