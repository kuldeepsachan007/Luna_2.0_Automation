# python
import io
import json
import base64
import contextlib
from pathlib import Path
from typing import Optional, Iterable, Iterator

import allure


class AllureLogger:
    """
    Helper to attach text, json, files and screenshots to Allure reports.

    Usage examples:
    - AllureLogger.attach_text("my log", "details")
    - AllureLogger.attach_json({"a": 1}, "response")
    - AllureLogger.attach_file(Path("/tmp/log.txt"), "server.log")
    - with AllureLogger.step("high level step"):
          AllureLogger.attach_text("step log", "info")
    """

    @staticmethod
    def attach_text(body: str, name: str = "text", extension: str = ".txt") -> None:
        """Attach a plain text blob."""
        allure.attach(body, name=name, attachment_type=allure.attachment_type.TEXT)

    @staticmethod
    def attach_json(obj, name: str = "json") -> None:
        """Attach a JSON-serializable object as application/json."""
        body = json.dumps(obj, indent=2, ensure_ascii=False)
        allure.attach(body, name=name, attachment_type=allure.attachment_type.JSON)

    @staticmethod
    def attach_bytes(data: bytes, name: str = "attachment", mime_type: str = "application/octet-stream") -> None:
        """Attach raw bytes with a specified mime type."""
        allure.attach(data, name=name, attachment_type=allure.utils._get_attachment_type_from_mime(mime_type))  # type: ignore

    @staticmethod
    def attach_file(path: Path, name: Optional[str] = None) -> None:
        """Attach a local file (binary) to Allure."""
        path = Path(path)
        if not path.exists():
            allure.attach(f"File not found: {path}", name=(name or "file_error"), attachment_type=allure.attachment_type.TEXT)
            return
        with path.open("rb") as f:
            data = f.read()
        attachment_name = name or path.name
        # Guess common types from suffix
        suffix = path.suffix.lower()
        if suffix in {".png", ".jpg", ".jpeg"}:
            atype = allure.attachment_type.PNG
        elif suffix in {".txt", ".log"}:
            atype = allure.attachment_type.TEXT
        elif suffix == ".json":
            atype = allure.attachment_type.JSON
        else:
            atype = allure.attachment_type.BINARY
        allure.attach(data, name=attachment_name, attachment_type=atype)

    @staticmethod
    def attach_screenshot_from_base64(b64: str, name: str = "screenshot") -> None:
        """Attach screenshot provided as base64 string (commonly returned by WebDriver)."""
        try:
            data = base64.b64decode(b64)
            allure.attach(data, name=name, attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            allure.attach(f"Failed to decode base64 screenshot: {e}", name=f"{name}_error", attachment_type=allure.attachment_type.TEXT)

    @staticmethod
    def attach_from_stream(stream: io.BytesIO, name: str = "stream", mime_type: str = "application/octet-stream") -> None:
        """Attach content from an io.BytesIO stream."""
        stream.seek(0)
        data = stream.read()
        try:
            if "png" in mime_type:
                atype = allure.attachment_type.PNG
            elif "json" in mime_type:
                atype = allure.attachment_type.JSON
            elif "text" in mime_type:
                atype = allure.attachment_type.TEXT
            else:
                atype = allure.attachment_type.BINARY
            allure.attach(data, name=name, attachment_type=atype)
        finally:
            stream.close()

    @staticmethod
    @contextlib.contextmanager
    def step(title: str) -> Iterator[None]:
        """Context manager for Allure steps.

        Example:
        with AllureLogger.step("do something"):
            AllureLogger.attach_text("inner log", "inner")
        """
        with allure.step(title):
            yield

    @staticmethod
    def attach_lines(lines: Iterable[str], name: str = "lines") -> None:
        """Attach iterable of text lines as a single text attachment."""
        body = "\n".join(str(l) for l in lines)
        allure.attach(body, name=name, attachment_type=allure.attachment_type.TEXT)
