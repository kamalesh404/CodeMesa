"""CodeMesa CLI entry point."""

from __future__ import annotations

import os
import sys

import click

from src.agents.orchestrator import Orchestrator
from src.core.state import SessionState
from src.llms import create_backend


def _make_orchestrator(output_dir: str | None) -> Orchestrator:
    state = SessionState()
    state.load()
    root = os.path.abspath(output_dir) if output_dir else state.get_project()
    if not root:
        raise click.ClickException(
            "No project set. Pass --dir or build a project first."
        )
    provider = os.environ.get("CODEMESA_BACKEND", "ollama")
    llm = create_backend(provider)
    if provider == "ollama":
        model = os.environ.get("CODEMESA_MODEL", "qwen2.5-coder:7b")
        llm.load(model)
    return Orchestrator(llm, root)


@click.group()
def cli() -> None:
    """CodeMesa — multi-agent AI project builder."""


@cli.command()
@click.argument("prompt")
@click.option("--dir", "-d", "output_dir", default=None, help="Output directory.")
def build(prompt: str, output_dir: str | None) -> None:
    """Build a complete project from scratch."""
    state = SessionState()
    state.load()
    root = os.path.abspath(output_dir) if output_dir else os.path.join(os.getcwd(), "generated")
    orch = _make_orchestrator(root)
    click.echo(f"Building project in {root} ...")
    summary = orch.build_from_scratch(prompt)
    state.set_project(root)
    click.echo(click.style(f"Done: {summary['files_written']}/{summary['files_planned']} files", fg="green"))
    if summary.get("tree"):
        click.echo(summary["tree"])


@cli.command()
@click.option("--dir", "-d", "output_dir", default=None)
def continue_build(output_dir: str | None) -> None:
    """Continue the last incomplete build."""
    orch = _make_orchestrator(output_dir)
    summary = orch.continue_build()
    click.echo(f"Continued: {summary['files_written']}/{summary['files_planned']} files")


@cli.command()
@click.option("--dir", "-d", "output_dir", default=None)
def status(output_dir: str | None) -> None:
    """Show the current project state."""
    orch = _make_orchestrator(output_dir)
    summary = orch.project.summary()
    click.echo(f"Project: {summary['name']}")
    click.echo(f"Path: {summary['root']}")
    click.echo(f"Files: {summary['files_written']}/{summary['files_planned']}")


if __name__ == "__main__":
    cli()
