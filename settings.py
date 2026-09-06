from pathlib import Path
from typing import Self, Any
from pydantic_settings import (
    BaseSettings, 
    SettingsConfigDict, 
    PydanticBaseSettingsSource, 
    JsonConfigSettingsSource
)

cwd = Path(__file__).resolve().parent


class Settings(BaseSettings): 
    model_config = SettingsConfigDict(
        env_file=cwd / ".env", 
        env_file_encoding='utf-8', 
        extra="allow", 
    )
    
    token: str 
    db_url: str
    unbelievaboat_key: str


class Conf(BaseSettings): 
    model_config = SettingsConfigDict(
        json_file=cwd / "json" / "conf.json",
        env_file_encoding='utf-8', 
        extra="allow", 
    )

    statuslist: list[str]
    log_channel_id: int
    shop_channels_ids: list[int]

    exchange_info: dict[str, dict[str, Any]]
    character_colors: dict[str, str]
    character_chances: dict[str, float]
    quartz_types: dict[str, str]
    quartz_emojis: dict[str, str]

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            JsonConfigSettingsSource(settings_cls),
            file_secret_settings,
        )

    @classmethod
    def reload(cls) -> Self:
        return cls.model_validate_json(
            Path(cwd / "json" / "conf.json").read_text(encoding="utf-8")
        )

class RollSchedule(BaseSettings): 
    model_config = SettingsConfigDict(
        json_file=cwd / "json" / "roll.json",
        env_file_encoding='utf-8', 
        extra="allow", 
    )

    common: dict[str, Any] #TODO BaseModel / dataclass
    negative: dict[str, Any] #TODO BaseModel / dataclass 
    gold: dict[str, Any] #TODO BaseModel / dataclass 

    @classmethod
    def reload(cls) -> Self:
        return cls.model_validate_json(
            Path(cwd / "json" / "roll.json").read_text(encoding="utf-8")
        )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            JsonConfigSettingsSource(settings_cls),
            file_secret_settings,
        )


settings = Settings() #type: ignore
conf = Conf.reload() #type: ignore
roll_schedule = RollSchedule.reload() #type: ignore