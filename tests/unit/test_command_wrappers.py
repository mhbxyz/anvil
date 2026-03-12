from collections import deque
from dataclasses import dataclass, field
from types import SimpleNamespace

from typer.testing import CliRunner

from flint.cli import app
from flint.scaffold import DevMode, ProfileCapabilities, RunMode
from flint.tooling import CommandResult, ToolKey


@dataclass(slots=True)
class FakeAdapters:
    config: object
    responses: deque[CommandResult]
    calls: list[tuple[ToolKey, tuple[str, ...]]] = field(default_factory=list)
    last_live_output: bool | None = None

    def run(
        self,
        key: ToolKey,
        args: tuple[str, ...] = (),
        cwd: None = None,
        *,
        live_output: bool = False,
    ) -> CommandResult:
        _ = cwd
        self.last_live_output = live_output
        self.calls.append((key, tuple(args)))
        return self.responses.popleft()

    def ensure_available(self, key: ToolKey) -> None:
        self.calls.append((key, ("__ensure__",)))


def _config(*, stop_on_first_failure: bool = True) -> SimpleNamespace:
    return SimpleNamespace(
        project=SimpleNamespace(name="myapi", profile="api", template="fastapi"),
        run=SimpleNamespace(app="myapi.main:app", host="127.0.0.1", port=8000),
        checks=SimpleNamespace(
            pipeline=("lint", "type", "test"),
            stop_on_first_failure=stop_on_first_failure,
        ),
    )


def _result(exit_code: int, stdout: str = "", stderr: str = "") -> CommandResult:
    return CommandResult(command=("tool",), exit_code=exit_code, stdout=stdout, stderr=stderr)


def test_lint_runs_default_args(monkeypatch) -> None:
    from flint.commands import lint

    adapters = FakeAdapters(config=_config(), responses=deque([_result(0)]))
    monkeypatch.setattr(lint, "build_adapters_or_exit", lambda: adapters)

    result = CliRunner().invoke(app, ["lint"])

    assert result.exit_code == 0
    assert adapters.calls == [(ToolKey.LINTING, ("check", "."))]
    assert "OK [lint]" in result.stdout


def test_lint_propagates_tool_exit_code(monkeypatch) -> None:
    from flint.commands import lint

    adapters = FakeAdapters(config=_config(), responses=deque([_result(7)]))
    monkeypatch.setattr(lint, "build_adapters_or_exit", lambda: adapters)

    result = CliRunner().invoke(app, ["lint"])

    assert result.exit_code == 7
    assert "FAILED [lint] exit code 7" in result.output


def test_install_runs_default_args(monkeypatch) -> None:
    from flint.commands import install

    adapters = FakeAdapters(config=_config(), responses=deque([_result(0)]))
    monkeypatch.setattr(install, "build_adapters_or_exit", lambda: adapters)

    result = CliRunner().invoke(app, ["install"])

    assert result.exit_code == 0
    assert adapters.calls == [(ToolKey.PACKAGING, ("sync", "--extra", "dev"))]
    assert "OK [install]" in result.output


def test_install_supports_passthrough_args(monkeypatch) -> None:
    from flint.commands import install

    adapters = FakeAdapters(config=_config(), responses=deque([_result(0)]))
    monkeypatch.setattr(install, "build_adapters_or_exit", lambda: adapters)

    result = CliRunner().invoke(app, ["install", "--frozen"])

    assert result.exit_code == 0
    assert adapters.calls == [(ToolKey.PACKAGING, ("--frozen",))]


def test_install_propagates_exit_code_with_actionable_error(monkeypatch) -> None:
    from flint.commands import install

    adapters = FakeAdapters(config=_config(), responses=deque([_result(4, stderr="sync failed")]))
    monkeypatch.setattr(install, "build_adapters_or_exit", lambda: adapters)

    result = CliRunner().invoke(app, ["install"])

    assert result.exit_code == 4
    assert "ERROR [tooling] Dependency sync failed" in result.output
    assert "Hint: Resolve backend errors above, then retry `flint install`." in result.output


def test_sync_alias_runs_default_args(monkeypatch) -> None:
    from flint.commands import install

    adapters = FakeAdapters(config=_config(), responses=deque([_result(0)]))
    monkeypatch.setattr(install, "build_adapters_or_exit", lambda: adapters)

    result = CliRunner().invoke(app, ["sync"])

    assert result.exit_code == 0
    assert adapters.calls == [(ToolKey.PACKAGING, ("sync", "--extra", "dev"))]
    assert "OK [sync]" in result.output


def test_run_uses_defaults_and_passthrough_args(monkeypatch) -> None:
    from flint.commands import run

    adapters = FakeAdapters(config=_config(), responses=deque([_result(0)]))
    monkeypatch.setattr(run, "build_adapters_or_exit", lambda: adapters)
    monkeypatch.setattr(
        run,
        "resolve_profile_capabilities_or_exit",
        lambda config: ProfileCapabilities(RunMode.SERVER, DevMode.SERVER_WITH_CHECKS),
    )

    result = CliRunner().invoke(app, ["run", "--reload"])

    assert result.exit_code == 0
    assert adapters.calls == [
        (
            ToolKey.RUNNING,
            ("myapi.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"),
        )
    ]
    assert adapters.last_live_output is True


def test_run_uses_config_overrides(monkeypatch) -> None:
    from flint.commands import run

    config = _config()
    config.run = SimpleNamespace(app="billing.main:app", host="0.0.0.0", port=9001)
    adapters = FakeAdapters(config=config, responses=deque([_result(0)]))
    monkeypatch.setattr(run, "build_adapters_or_exit", lambda: adapters)
    monkeypatch.setattr(
        run,
        "resolve_profile_capabilities_or_exit",
        lambda config: ProfileCapabilities(RunMode.SERVER, DevMode.SERVER_WITH_CHECKS),
    )

    result = CliRunner().invoke(app, ["run"])

    assert result.exit_code == 0
    assert adapters.calls == [
        (
            ToolKey.RUNNING,
            ("billing.main:app", "--host", "0.0.0.0", "--port", "9001"),
        )
    ]


def test_run_propagates_exit_code_and_shows_app_hint(monkeypatch) -> None:
    from flint.commands import run

    stderr = 'ERROR:    Error loading ASGI app. Could not import module "wrong.module".'
    adapters = FakeAdapters(config=_config(), responses=deque([_result(7, stderr=stderr)]))
    monkeypatch.setattr(run, "build_adapters_or_exit", lambda: adapters)
    monkeypatch.setattr(
        run,
        "resolve_profile_capabilities_or_exit",
        lambda config: ProfileCapabilities(RunMode.SERVER, DevMode.SERVER_WITH_CHECKS),
    )

    result = CliRunner().invoke(app, ["run"])

    assert result.exit_code == 7
    assert "ERROR [tooling] Failed to run ASGI app `myapi.main:app`." in result.output
    assert "Hint: Check `[run].app` in `flint.toml`" in result.output


def test_run_executes_cli_profile_via_python_module(monkeypatch) -> None:
    from flint.commands import run

    config = _config()
    config.project = SimpleNamespace(name="Billing CLI", profile="cli")
    adapters = FakeAdapters(config=config, responses=deque([_result(0)]))
    monkeypatch.setattr(run, "build_adapters_or_exit", lambda: adapters)
    monkeypatch.setattr(
        run,
        "resolve_profile_capabilities_or_exit",
        lambda config: ProfileCapabilities(RunMode.CLI, DevMode.CHECKS_ONLY),
    )

    result = CliRunner().invoke(app, ["run", "--verbose"])

    assert result.exit_code == 0
    assert adapters.calls == [(ToolKey.RUNNING, ("-m", "billing_cli.main", "--verbose"))]
    assert "Starting CLI process..." in result.output


def test_run_rejects_unsupported_profile(monkeypatch) -> None:
    from flint.commands import run

    config = _config()
    config.project = SimpleNamespace(name="mylib", profile="lib")
    adapters = FakeAdapters(config=config, responses=deque())
    monkeypatch.setattr(run, "build_adapters_or_exit", lambda: adapters)
    monkeypatch.setattr(
        run,
        "resolve_profile_capabilities_or_exit",
        lambda config: ProfileCapabilities(RunMode.UNSUPPORTED, DevMode.CHECKS_ONLY),
    )

    result = CliRunner().invoke(app, ["run"])

    assert result.exit_code == 2
    assert "`flint run` is not supported for profile `lib`." in result.output


def test_check_runs_full_pipeline_and_reports_summary(monkeypatch) -> None:
    from flint.commands import check

    adapters = FakeAdapters(
        config=_config(stop_on_first_failure=False),
        responses=deque([_result(0), _result(3), _result(0)]),
    )
    monkeypatch.setattr(check, "build_adapters_or_exit", lambda: adapters)

    result = CliRunner().invoke(app, ["check"])

    assert result.exit_code == 3
    assert adapters.calls == [
        (ToolKey.LINTING, ("check", ".")),
        (ToolKey.TYPING, ()),
        (ToolKey.TESTING, ()),
    ]
    assert "CHECK SUMMARY: failed step(s): type" in result.output


def test_dev_requires_running_tool_for_server_profile(monkeypatch) -> None:
    from flint.commands import dev

    adapters = FakeAdapters(config=_config(), responses=deque())
    ensure_calls: list[ToolKey] = []
    monkeypatch.setattr(dev, "build_adapters_or_exit", lambda: adapters)
    monkeypatch.setattr(
        dev,
        "resolve_profile_capabilities_or_exit",
        lambda config: ProfileCapabilities(RunMode.SERVER, DevMode.SERVER_WITH_CHECKS),
    )
    monkeypatch.setattr(dev, "ensure_tool_available_or_exit", lambda adapters, key: ensure_calls.append(key))
    monkeypatch.setattr(dev, "run_dev_loop", lambda adapters, mode: None)

    result = CliRunner().invoke(app, ["dev"])

    assert result.exit_code == 0
    assert ensure_calls == [
        ToolKey.RUNNING,
        ToolKey.LINTING,
        ToolKey.TYPING,
        ToolKey.TESTING,
    ]


def test_dev_skips_running_tool_in_checks_only_mode(monkeypatch) -> None:
    from flint.commands import dev

    adapters = FakeAdapters(config=_config(), responses=deque())
    ensure_calls: list[ToolKey] = []
    dev_modes: list[DevMode] = []
    monkeypatch.setattr(dev, "build_adapters_or_exit", lambda: adapters)
    monkeypatch.setattr(
        dev,
        "resolve_profile_capabilities_or_exit",
        lambda config: ProfileCapabilities(RunMode.CLI, DevMode.CHECKS_ONLY),
    )
    monkeypatch.setattr(dev, "ensure_tool_available_or_exit", lambda adapters, key: ensure_calls.append(key))
    monkeypatch.setattr(dev, "run_dev_loop", lambda adapters, mode: dev_modes.append(mode))

    result = CliRunner().invoke(app, ["dev"])

    assert result.exit_code == 0
    assert ensure_calls == [ToolKey.LINTING, ToolKey.TYPING, ToolKey.TESTING]
    assert dev_modes == [DevMode.CHECKS_ONLY]


def test_dev_rejects_unsupported_profile(monkeypatch) -> None:
    from flint.commands import dev

    config = _config()
    config.project = SimpleNamespace(name="demo", profile="worker", template="baseline-worker")
    adapters = FakeAdapters(config=config, responses=deque())
    monkeypatch.setattr(dev, "build_adapters_or_exit", lambda: adapters)
    monkeypatch.setattr(
        dev,
        "resolve_profile_capabilities_or_exit",
        lambda config: ProfileCapabilities(RunMode.UNSUPPORTED, DevMode.UNSUPPORTED),
    )

    result = CliRunner().invoke(app, ["dev"])

    assert result.exit_code == 2
    assert "`flint dev` is not supported for profile `worker`." in result.output
