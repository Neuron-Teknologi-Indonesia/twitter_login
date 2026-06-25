from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Type

from ..utils import optional_chaining, safe_convert
from .base import model
from .card import Card
from .lazy import Lazy, LazyMixin
from .notetweet import NoteTweet
from .tweet_entities import TweetEntitiesMixin
from .user import User

if TYPE_CHECKING:
    from .tweet_entities import URL, Hashtag, Mention, Symbol
    from ..client import Client


@model(reprs='id')
class Tweet(TweetEntitiesMixin, LazyMixin):
    _client: Client
    #: The unique identifier of the tweet.
    id: str
    #: The state of the tweet views.
    view_count: int
    #: The count of bookmarks for the tweet.
    bookmark_count: int
    #: Indicates if the tweet is bookmarked.
    bookmarked: bool
    #: The date and time when the tweet was created.
    created_at: str
    #: The count of favorites for the tweet.
    favorite_count: int
    #: Indicates if the tweet is favorited.
    favorited: bool
    #: The text of the tweet. Use :attr:`.full_text` to get full text.
    text: str
    #: Indicates if the tweet is a quote tweet.
    is_quote_status: bool
    in_reply_to_screen_name: str | None
    in_reply_to_user_id: str | None
    #: The language of the tweet.
    lang: str
    #: The count of quotes for the tweet.
    quote_count: int
    #: The count of replies to the tweet.
    reply_count: int
    #: The count of retweets for the tweet.
    retweet_count: int
    #: Indicates if the tweet is retweeted.
    retweeted: bool
    #: ID of the author user.
    user_id: str
    source: str
    #: The conversation id.
    conversation_id: str

    #: Author of the tweet.
    user: ClassVar[User | None] = Lazy(
        User,
        kwargs_factory=lambda x: {'client': x._client}
    )
    note_tweet: ClassVar[NoteTweet | None] = Lazy(NoteTweet)
    card: ClassVar[Card | None] = Lazy(Card)

    @classmethod
    def _from_payload(cls: Type['Tweet'], payload: dict, client: Client, user: User | None = None):
        legacy = payload.get('legacy', {})
        views = payload.get('views', {})

        instance = cls(
            _client=client,
            id=payload.get('rest_id'),
            view_count=safe_convert(views.get('count', 0), int),
            bookmark_count=legacy.get('bookmark_count'),
            bookmarked=legacy.get('bookmarked'),
            created_at=legacy.get('created_at'),
            favorite_count=legacy.get('favorite_count'),
            favorited=legacy.get('favorited'),
            text=legacy.get('full_text'),
            is_quote_status=legacy.get('is_quote_status'),
            in_reply_to_screen_name=legacy.get('in_reply_to_screen_name'),
            in_reply_to_user_id=legacy.get('in_reply_to_user_id_str'),
            lang=legacy.get('lang'),
            quote_count=legacy.get('quote_count'),
            reply_count=legacy.get('reply_count'),
            retweet_count=legacy.get('retweet_count'),
            retweeted=legacy.get('retweeted'),
            user_id=legacy.get('user_id_str'),
            source=payload.get('source'),
            conversation_id=legacy.get('conversation_id_str')
        )

        if not user:
            user = optional_chaining(payload, 'core', 'user_results', 'result')

        instance.user = user

        note_tweet = optional_chaining(payload, 'note_tweet', 'note_tweet_results', 'result')

        instance.note_tweet = note_tweet
        instance.card = payload.get('card')

        entities = legacy.get('entities', {})
        instance._set_sources_from_entities(entities)

        return instance

    def __fallback_to_note(self, attr_name):
        if self.note_tweet:
            return getattr(self.note_tweet, attr_name)
        return getattr(self, attr_name)

    @property
    def full_text(self) -> str:
        return self.__fallback_to_note('text')

    @property
    def full_urls(self) -> list[URL]:
        return self.__fallback_to_note('urls')

    @property
    def full_hashtags(self) -> list[Hashtag]:
        return self.__fallback_to_note('hashtags')

    @property
    def full_symbols(self) -> list[Symbol]:
        return self.__fallback_to_note('symbols')

    @property
    def full_mentions(self) -> list[Mention]:
        return self.__fallback_to_note('mentions')
