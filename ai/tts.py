import os
import signal
import subprocess

from config.config import Config


class TextToSpeech:
    """
    Base class for all text-to-speech implementations
    """

    def speak_text(self, text: str):
        pass

    def cancel(self):
        pass

    def is_playing(self) -> bool:
        pass

    def is_paused(self) -> bool:
        pass

    def pause(self):
        pass

    def resume(self):
        pass


class CmdTextToSpeech(TextToSpeech):
    """
    Implements TTS by running a local script, provided by a config option. It allows
    users to specify a working TTS command that they have installed locally that will
    generate and play audio for the text. For instance, in MacOS, the `say` cmd utility
    can be used for a single and performant TTS
    """

    config = Config()
    text_marker = '<text>'

    def __init__(self):
        super().__init__()
        self.subprocess: subprocess.Popen | None = None
        self.is_process_suspended: bool = False

    def speak_text(self, text: str):
        if not self.config.tts or not self.config.tts.cmd:
            return
        command = self.config.tts.cmd.replace(self.text_marker, text)
        process = subprocess.Popen(command, shell=True)
        self.subprocess = process
        self.is_process_suspended = False

    def cancel(self):
        if self.subprocess and self.subprocess.poll() is None:  # Check if the process is still running
            self.subprocess.terminate()  # Terminate the process
            self.subprocess.wait()  # Wait for the process to terminate
            self.is_process_suspended = False

    def is_playing(self) -> bool:
        return self.subprocess and self.subprocess.poll() is None

    def pause(self):
        if self.subprocess and self.subprocess.poll() is None:
            os.kill(self.subprocess.pid, signal.SIGSTOP)
            self.is_process_suspended = True

    def resume(self):
        if self.subprocess and self.subprocess.poll() is None:
            os.kill(self.subprocess.pid, signal.SIGCONT)
            self.is_process_suspended = False

    def is_paused(self) -> bool:
        """
        Checks if there's a suspended speech command
        :return: Yes, if playback can be resumed
        """
        # also checks for an existing subprocess that hasn't exited yet as a double check
        return self.subprocess and self.subprocess.poll() is None and self.is_process_suspended


def has_tts_setup() -> bool:
    """
    Determines if the application has text-to-speech configured (based on the configuration).
    :return: True, if the config contains options for using TTS, or False otherwise
    """
    config = Config()
    return config.tts is not None


def speak_text(text: str) -> TextToSpeech:
    """
    Uses the configured TTS options in order to say the provided text
    :param text: The text to say
    :return: A TextToSpeech instance that can be used to stop the audio
    """
    # so far, only TTS based on a custom command is supported
    tts = CmdTextToSpeech()
    tts.speak_text(text)
    return tts
