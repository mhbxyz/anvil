from dataclasses import dataclass


@dataclass(slots=True)
class FlintError(Exception):
    message: str
    hint: str
    category: str
    exit_code: int

    def render(self) -> tuple[str, str]:
        return (
            f"ERROR [{self.category}] {self.message}",
            f"Hint: {self.hint}",
        )


def usage_error(message: str, hint: str) -> FlintError:
    return FlintError(message=message, hint=hint, category="usage", exit_code=2)


def config_error(message: str, hint: str) -> FlintError:
    return FlintError(message=message, hint=hint, category="config", exit_code=2)


def tooling_error(message: str, hint: str) -> FlintError:
    return FlintError(message=message, hint=hint, category="tooling", exit_code=1)
