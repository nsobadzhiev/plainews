from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource, YamlConfigSettingsSource


class HistoryConfig(BaseModel):
    keep_history: bool | None = False
    max_history_items_per_feed: int | None = 150


class TextToSpeechConfig(BaseModel):
    cmd: str | None = None


class Config(BaseSettings):
    llm_model: str = "ollama/llama3.1"
    llm_base_url: str | None = None   # "http://localhost:11434" for Ollama
    llm_api_key: str | None = ""
    language: str = "english"
    feeds_file: str = '../feeds.pickle'
    session_file: str = 'session.pickle'
    transformers: list[str] = []
    followed_feeds: list[str] = [
        "https://rss.sueddeutsche.de/rss/Topthemen",
        "https://feeds.arstechnica.com/arstechnica/index",
    ]
    summarization_target_length: int | None = 250
    history: HistoryConfig = HistoryConfig()
    tts: TextToSpeechConfig | None = None

    # There are two options - reading the config from a file in the PWD, or reading
    # a file from the home directory
    model_config = SettingsConfigDict(yaml_file=['~/.plainews.yml', 'config.yml'])

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """
        This overridden method is needed in order to include the Yaml source
        into the list while initializing
        :param settings_cls:
        :param init_settings:
        :param env_settings:
        :param dotenv_settings:
        :param file_secret_settings:
        :return:
        """
        return (
            YamlConfigSettingsSource(settings_cls),
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )
