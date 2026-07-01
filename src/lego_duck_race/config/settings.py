import os
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)


class LaneConfig(BaseModel):
    """Configuration for one race lane.

    The lane name is also the Build HAT motor port and limit-switch mapping key.
    """

    model_config = ConfigDict(frozen=True)

    name: str = Field(min_length=1)
    button_name: str = Field(min_length=1)
    limit_switch_gpio: int = Field(gt=0)

    @property
    def motor_port(self) -> str:
        return self.name

    @property
    def switch_name(self) -> str:
        return self.name


LANE_CONFIG_ENV_VAR = "LEGO_DUCK_RACE_LANE_CONFIG"


def load_lane_configs() -> list[LaneConfig]:
    default_config_path = Path(__file__).parent.resolve().joinpath("lanes.yaml")
    config_path = Path(os.environ.get(LANE_CONFIG_ENV_VAR) or default_config_path)

    class LaneSettings(BaseSettings):
        model_config = SettingsConfigDict(env_prefix="LEGO_DUCK_RACE_")

        lanes: list[LaneConfig]

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
                YamlConfigSettingsSource(settings_cls, yaml_file=config_path),
                dotenv_settings,
                file_secret_settings,
            )

    return LaneSettings().lanes  # ty:ignore[missing-argument]


DEFAULT_LANES = load_lane_configs()
