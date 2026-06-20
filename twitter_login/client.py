from __future__ import annotations

import json
from pathlib import Path

from .api import API
from .auth_manager import AuthManager
from .gql_endpoints import GQLEndpointsManager
from .http import HTTPClient
from .mixins import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .headers import UserAgent


class Client(SearchMixin, TweetMixin, MediaMixin):
    def __init__(self, user_agent: UserAgent, impersonate: str, *args, **kwargs):
        http = HTTPClient(user_agent, impersonate=impersonate, *args, **kwargs)
        self._gql_endpoints_manager = GQLEndpointsManager(http)
        self._api = API(http, self._gql_endpoints_manager.state)
        self._auth_manager = AuthManager(http, self._api)
        self.ratelimits = http.ratelimits_manager

    async def load_cookies(
        self,
        cookies: str | Path | dict[str, str],
        *,
        update_gql_endpoints: bool = True,
        validate_cookies: bool = True
    ) -> None:
        """Logs in using the provided cookies.

        Parameters
        ----------
        cookies : :class:`str` | :class:`Path` | dict[:class:`str`, :class:`str`]
            A path to the cookies JSON file, or a dictionary of cookies.
            The dictionary must follow a key-value format.
        update_gql_endpoints : :class:`bool`, default=True
            Whether to fetch and update the latest GraphQL endpoints.
        validate_cookies : :class:`bool`, default=True
            Whether to validate cookie authentication.

        Raises
        ------
        TypeError
            Unsupported cookies type.
        """
        if isinstance(cookies, (str, Path)):
            with open(cookies, encoding='utf-8') as f:
                cookies = json.load(f)

        if not isinstance(cookies, dict):
            raise TypeError(f'Cookies must be dict, not {cookies.__class__.__name__}.')

        await self._auth_manager.login_with_cookies(cookies, validate_cookies=validate_cookies)
        # Update GQL endpoints
        if update_gql_endpoints:
            await self._gql_endpoints_manager.update_state()

    def save_cookies(self, path: str | Path):
        """
        Saves the cookies to the specific file.

        Parameters
        ----------
        path : :class:`str` | :class:`pathlib.Path`
            A path to the file to save.
        """
        self._auth_manager.save_cookies(path)
