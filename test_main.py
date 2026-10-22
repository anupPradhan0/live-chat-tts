import asyncio
import io
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from aiohttp import WSServerHandshakeError

import main


class SpeechFailureTests(unittest.TestCase):
    def test_chat_continues_after_speech_handshake_failure(self):
        chat = Mock()
        chat.is_alive.side_effect = [True, False]
        chat.get.return_value.sync_items.return_value = [
            SimpleNamespace(author=SimpleNamespace(name="viewer"), message=message)
            for message in ("first", "second")
        ]
        error = WSServerHandshakeError(None, (), status=403, message="Forbidden")
        with (
            patch.object(main.sys, "argv", ["live-chat", "https://youtube.com/watch?v=test"]),
            patch.object(main.pytchat, "create", return_value=chat),
            patch.object(main, "speak", new_callable=AsyncMock) as speak,
            patch.object(main.time, "sleep"),
            patch("sys.stdout", new_callable=io.StringIO),
            patch("sys.stderr", new_callable=io.StringIO) as stderr,
        ):
            speak.side_effect = [error, None]
            main.main()
            self.assertEqual(speak.await_count, 2)
            self.assertIn("continuing chat", stderr.getvalue())
            self.assertNotIn("Traceback", stderr.getvalue())

    def test_failed_synthesis_removes_partial_audio_without_playing(self):
        paths = []

        async def fail_save(filename):
            path = Path(filename)
            paths.append(path)
            path.write_bytes(b"partial audio")
            raise OSError("connection lost")

        with (
            patch.object(main.edge_tts, "Communicate") as communicate,
            patch.object(main.subprocess, "run") as play,
        ):
            communicate.return_value.save = AsyncMock(side_effect=fail_save)
            with self.assertRaises(OSError):
                asyncio.run(main.speak("hello"))
            play.assert_not_called()
        self.assertFalse(paths[0].exists())
        self.assertFalse(paths[0].parent.exists())


if __name__ == "__main__":
    unittest.main()
