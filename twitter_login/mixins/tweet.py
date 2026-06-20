from ..enums import BatchCompose, ConversationControl
from ..models.tweet import Tweet
from ..models.uploaded_media import UploadedMedia
from ..parsers import handle_response_errors
from ..utils import optional_chaining
from .base import BaseMixin


def build_tweet_media_parameter(media: list[UploadedMedia], tagged_users: list[str]):
    media_entities = []
    for m in media:
        if not isinstance(m, UploadedMedia):
            raise TypeError('Media must be an instance of `UploadedMedia`.')

        media_entities.append({
            'media_id': m.media_id,
            'tagged_users': tagged_users
        })
    return {
        'media_entities': media_entities,
        'possibly_sensitive': False
    }


class TweetMixin(BaseMixin):
    async def create_tweet(
        self,
        text: str = '',
        # card = None,
        attachment_url: str | None = None,
        reply_to: str | None = None,
        exclude_reply_user_ids: list[str] | None = None,
        batch_compose: BatchCompose = BatchCompose.SINGLE_TWEET,
        # geo = None,
        media: list[UploadedMedia] | None = None,
        tagged_users: list[str] | None = None,
        conversation_control: ConversationControl | None = None
    ):
        if batch_compose == BatchCompose.SINGLE_TWEET:
            batch_compose = None

        media_param = build_tweet_media_parameter(
            media or [], tagged_users or []
        )

        reply = None
        if reply_to:
            reply = {
                'in_reply_to_tweet_id': reply_to,
                'exclude_reply_user_ids': exclude_reply_user_ids or []
            }

        response = await self._api.gql.CreateTweet(
            tweet_text=text,
            card_uri=None,
            attachment_url=attachment_url,
            reply=reply,
            batch_compose=batch_compose,
            geo=None,
            media=media_param,
            conversation_control={'mode': conversation_control} if conversation_control else None
        )

        payload = response.json()
        handle_response_errors(payload)
        tweet_payload = optional_chaining(
            payload, 'data', 'create_tweet', 'tweet_results', 'result'
        )
        return Tweet._from_payload(tweet_payload, self)
