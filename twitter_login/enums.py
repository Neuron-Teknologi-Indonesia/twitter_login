from enum import Enum


class StrEnum(str, Enum):
    """
    :meta private:
    """
    def __str__(self) -> str:
        return str(self.value)


class UserState(StrEnum):
    """
    :meta private:
    """
    NORMAL = 'normal'
    SUSPENDED = 'suspended'
    NOT_LOGGED_IN = 'not_logged_in'


class MediaState(StrEnum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'


class MediaCategory(StrEnum):
    AMPLIFY_VIDEO = 'amplify_video'
    COMMUNITY_BANNER = 'community_banner_image'
    LIST_BANNER = 'list_banner_image'
    TWEET_IMAGE = 'tweet_image'
    TWEET_VIDEO = 'tweet_video'
    TWEET_GIF = 'tweet_gif'
    DM_IMAGE = 'dm_image'
    DM_VIDEO = 'dm_video'
    DM_GIF = 'dm_gif'
    SUBTITLES = 'subtitles'
    PROFILE_BANNER = 'banner_image'
    CARD_IMAGE = 'card_image'


class SensitiveMediaWarning(StrEnum):
    ADULT_CONTENT = 'adult_content'
    GRAPHIC_VIOLENCE = 'graphic_violence'
    OTHER = 'other'


class BatchCompose(StrEnum):
    SINGLE_TWEET = 'off'
    FIRST_TWEET = 'first'
    SUBSEQUENT_TWEET = 'subsequent'


class ConversationControl(StrEnum):
    COMMUNITY = 'Community'
    BY_INVITATION = 'ByInvitation'
    SUBSCRIBERS = 'Subscribers'
    VERIFIED = 'Verified'
    PREMIUM = 'Premium'


class SearchTimelineParam(StrEnum):
    """
    :meta private:
    Search timeline URL f= parameters
    """
    IMAGE = 'image'
    LIST = 'list'
    LIVE = 'live'
    MEDIA = 'media'
    TOP = 'top'
    USER = 'user'
    VIDEO = 'video'


class SearchTimelineProduct(StrEnum):
    IMAGE = 'Photos'
    LIST = 'Lists'
    MEDIA = 'Media'
    TOP = 'Top'
    USER = 'People'
    VIDEO = 'Videos'
    LATEST = 'Latest'


SEARCH_TIMELINE_PRODUCT_TO_PARAM = {
    SearchTimelineProduct.IMAGE: SearchTimelineParam.IMAGE,
    SearchTimelineProduct.LIST: SearchTimelineParam.LIST,
    SearchTimelineProduct.MEDIA: SearchTimelineParam.MEDIA,
    SearchTimelineProduct.TOP: SearchTimelineParam.TOP,
    SearchTimelineProduct.USER: SearchTimelineParam.USER,
    SearchTimelineProduct.VIDEO: SearchTimelineParam.VIDEO,
    SearchTimelineProduct.LATEST: SearchTimelineParam.LIVE
}


class SearchTimelineQuerySource(StrEnum):
    ADVANCED_SEARCH_PAGE = 'advanced_search_page'
    CASHTAG_CLICK = 'cashtag_click'
    HASHTAG_CLICK = 'hashtag_click'
    PROMOTED_TREND_CLICK = 'promoted_trend_click'
    RECENT_SEARCH_CLICK = 'recent_search_click'
    RELATED_QUERY_CLICK = 'related_query_click'
    SPELLING_CORRECTION_CLICK = 'spelling_correction_click'
    SPELLING_CORRECTION_REVERT_CLICK = 'spelling_suggestion_revert_click'
    SPELLING_EXPANSION_CLICK = 'spelling_expansion_click'
    SPELLING_EXPANSION_REVERT_CLICK = 'spelling_expansion_revert_click'
    SPELLING_SUGGESTION_CLICK = 'spelling_suggestion_click'
    TREND_CLICK = 'trend_click'
    TREND_VIEW = 'trend_view'
    TYPEAHEAD_CLICK = 'typeahead_click'
    TYPED = 'typed_query'
    TV_SEARCH = 'TvSearch'
    TWEET_DETAIL_QUOTE_TWEET = 'tdqt'
    TWEET_DETAIL_SIMILAR_POST = 'tweet_detail_similar_posts'


class InstructionType(StrEnum):
    """
    :meta private:
    """
    # Timeline
    TIMELINE_ADD_ENTRIES = 'TimelineAddEntries'
    TIMELINE_REMOVE_ENTRIES = 'TimelineRemoveEntries'
    TIMELINE_REPLACE_ENTRY = 'TimelineReplaceEntry'
    TIMELINE_ADD_TO_MODULE = 'TimelineAddToModule'
    TIMELINE_PIN_ENTRY = 'TimelinePinEntry'
    TIMELINE_SHOW_COVER = 'TimelineShowCover'
    TIMELINE_TERMINATE_TIMELINE = 'TimelineTerminateTimeline'
    TIMELINE_CLEAR_CACHE = 'TimelineClearCache'
    TIMELINE_SHOW_ALERT = 'TimelineShowAlert'
    TIMELINE_NAVIGATION = 'TimelineNavigation'
    TIMELINE_CLEAR_ENTRIES_UNREAD_STATE = 'TimelineClearEntriesUnreadState'
    TIMELINE_MARK_ENTRIES_UNREAD_GREATER_THAN_SORT_INDEX = 'TimelineMarkEntriesUnreadGreaterThanSortIndex'
