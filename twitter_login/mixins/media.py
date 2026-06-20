from io import BufferedIOBase
from logging import getLogger
from pathlib import Path

from ..enums import MediaCategory
from ..errors import MediaUploadError
from ..media import MediaUploader
from ..models.uploaded_media import UploadedMedia
from .base import BaseMixin

logger = getLogger(__name__)


class MediaMixin(BaseMixin):
    async def upload_media(
        self,
        source: str | Path | bytes | BufferedIOBase,
        media_category: MediaCategory,
        mimetype: str | None = None,
        concurrency: int = 6,
        enable_video_duration: bool = True,
        wait_for_completion: bool = True,
        timeout: int = 100
    ) -> UploadedMedia:
        """
        Uploads media
        """
        uploader = MediaUploader(
            self._api, source, media_category,
            mimetype=mimetype,
            concurrency=concurrency,
            enable_video_duration=enable_video_duration
        )
        finalize_payload = await uploader.upload()
        logger.info(f'Upload finalized: {finalize_payload}')
        media = UploadedMedia._from_payload(finalize_payload, self, media_category)

        if not media.processing_info:
            if not media.content:
                raise MediaUploadError(f'Failed to upload media: "{finalize_payload}"')
            return media

        if wait_for_completion:
            await media.wait_for_completion(timeout)
        return media
