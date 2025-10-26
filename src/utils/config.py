import tomllib
from typing import List, Optional
from sqlalchemy import URL
from pydantic import BaseModel, Field


class AppEmulatorConfig(BaseModel):
    flow_size: int = Field(
        default=1, description="Number of iterations the emulator should run"
    )


class DatabaseConfig(BaseModel):
    name: str = Field(description="Database connection name/identifier")
    protocol: str = Field(default="postgresql", description="Database protocol/driver")
    host: str = Field(default="localhost", description="Database host")
    port: int = Field(default=5432, description="Database port")
    username: str = Field(default="user", description="Database username")
    password: str = Field(default="password", description="Database password")
    database: str = Field(default="sample_db", description="Database name")

    @property
    def connection_url(self) -> str:
        """Generate SQLAlchemy connection URL."""
        return URL.create(
            drivername=self.protocol,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )


class LoggerConfig(BaseModel):
    level: str = Field(default="INFO", description="Logging level")
    file: Optional[str] = Field(None, description="Log file path")
    name: str = Field(description="Logger name")
    line_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log line format",
    )


class LoggingConfig(BaseModel):
    """Logging configuration."""

    level: str = Field(default="WARNING", description="Global logging level")
    line_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log line format",
    )
    loggers: List[LoggerConfig] = Field(
        default=[LoggerConfig(name="flow"), LoggerConfig(name="emulator")]
    )


class AppConfig(BaseModel):
    """Main application configuration."""

    emulator: AppEmulatorConfig
    databases: List[DatabaseConfig] = Field(default_factory=list)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)

    def get_database(self, name: str) -> DatabaseConfig | None:
        """Get database config by name."""
        for db in self.databases:
            if db.name == name:
                return db
        return None

    def get_database_names(self) -> List[str]:
        """Get list of all database names."""
        return [db.name for db in self.databases]


def load_config(file_path: str) -> AppConfig:
    """Load configuration from TOML file."""
    with open(file_path, "rb") as f:
        toml_data = tomllib.load(f)

    # Parse emulator config
    emulator_config = AppEmulatorConfig(**toml_data.get("emulator", {}))

    # Parse database configs from [[database]] array
    database_configs = []
    for db_data in toml_data.get("database", []):
        database_configs.append(DatabaseConfig(**db_data))

    return AppConfig(emulator=emulator_config, databases=database_configs)
