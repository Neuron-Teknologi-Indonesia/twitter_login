from typing import Any, Literal, overload

from ..enums import InstructionType, SearchTimelineProduct, SearchTimelineQuerySource
from ..models.tweet import Tweet
from ..models.user import User
from ..pagination import PaginatedResult, PaginationContext
from ..parsers import (
    get_cursors_from_entries,
    get_cursors_from_replace_entries,
    get_instructions,
    group_entries,
    handle_response_errors,
    parse_entries
)
from ..utils import optional_chaining
from .base import BaseMixin


class SearchMixin(BaseMixin):
    @overload
    async def search(
        self,
        query: str,
        product: Literal[SearchTimelineProduct.USER],
        count: int = ...,
        cursor: str | None = ...,
        query_source: SearchTimelineQuerySource = ...
    ) -> PaginatedResult[User]:
        ...

    @overload
    async def search(
        self,
        query: str,
        product: Literal[
            SearchTimelineProduct.LIVE,
            SearchTimelineProduct.TOP,
            SearchTimelineProduct.MEDIA,
            SearchTimelineProduct.IMAGE,
            SearchTimelineProduct.VIDEO
        ],
        count: int = ...,
        cursor: str | None = ...,
        query_source: SearchTimelineQuerySource = ...
    ) -> PaginatedResult[Tweet]:
        ...

    async def search(
        self,
        query: str,
        product: SearchTimelineProduct,
        count: int = 20,
        cursor: str | None = None,
        query_source: SearchTimelineQuerySource = SearchTimelineQuerySource.TYPED
    ) -> PaginatedResult[Any]:
        response = await self._api.gql.SearchTimeline(
            rawQuery=query,
            count=count,
            cursor=cursor,
            querySource=query_source,
            product=product
        )
        payload = response.json()
        handle_response_errors(payload)

        instructions = get_instructions(
            payload, 'data', 'search_by_raw_query', 'search_timeline', 'timeline', 'instructions'
        )

        if InstructionType.TIMELINE_ADD_ENTRIES not in instructions:
            return PaginatedResult._empty()

        # Extract TimelineAddEntries entries from instructions
        entries = group_entries(
            instructions.get(InstructionType.TIMELINE_ADD_ENTRIES)[0]['entries']
        )
        replace_entry_instructions = instructions.get(InstructionType.TIMELINE_REPLACE_ENTRY)


        if InstructionType.TIMELINE_ADD_TO_MODULE in instructions:
            add_to_module = instructions[InstructionType.TIMELINE_ADD_TO_MODULE][0]
            module_type = add_to_module['moduleEntryId']

            if module_type.startswith('search-grid'):
                # MEDIA with a cursor
                cursor_top, cursor_bottom = get_cursors_from_replace_entries(
                    replace_entry_instructions
                )
                if 'moduleItems' not in add_to_module:
                    raise ValueError('moduleItems not found in "search-grid"')
                entry_results = add_to_module['moduleItems']

            elif module_type.startswith('list-search'):
                # LIST with a cursor
                return PaginatedResult._empty()  ## TODO List support

            else:
                raise ValueError(f'Unknown moduleEntryId "{module_type}"')


        else:
            if 'search-grid' in entries:
                # MEDIA without a cursor
                cursor_top, cursor_bottom = get_cursors_from_entries(entries)
                items = optional_chaining(entries['search-grid'][0], 'content', 'items')
                if not items:
                    raise ValueError('Items not found in "search-grid"')
                entry_results = group_entries(items)['search-grid-0-tweet']

            elif 'list-search' in entries:
                # LIST without a cursor
                return PaginatedResult._empty()  ## TODO List support

            else:
                if ('cursor-top' in entries or 'cursor-bottom' in entries):
                    # LATEST or TOP without a cursor
                    cursor_top, cursor_bottom = get_cursors_from_entries(entries)

                else:
                    # LATEST or TOP with a cursor
                    cursor_top, cursor_bottom = get_cursors_from_replace_entries(
                        replace_entry_instructions
                    )

                if product == SearchTimelineProduct.USER:
                    entry_results = entries['user']
                else:
                    entry_results = entries['tweet']

        items_iter = parse_entries(self, entry_results)
        ctx = PaginationContext(
            self,
            SearchMixin.search,
            cursor_top,
            cursor_bottom,
            # params
            query=query,
            product=product,
            count=count,
            query_source=query_source
        )
        return PaginatedResult(items_iter, ctx)
