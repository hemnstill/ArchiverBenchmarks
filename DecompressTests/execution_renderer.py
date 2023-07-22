import os.path
import sys

import pygal
from airium import Airium

from DecompressTests import models, common_paths, io_tools


def render(execution_infos: list[models.ExecutionInfo]) -> None:
    a = Airium()

    a('<!DOCTYPE html>')
    with a.html(lang="en"):
        with a.head():
            a.meta(charset="utf-8")
            a.title(_t="Execution info")

        with a.body(style="margin: 0;"):
            _render_execution(a, execution_infos)

    io_tools.write_text(os.path.join(common_paths.render_path, 'index.html'), str(a))


def _render_execution(a: Airium, execution_infos: list[models.ExecutionInfo]):
    os.makedirs(common_paths.render_path, exist_ok=True)

    bar_chart = pygal.Bar()
    bar_chart.title = sys.platform

    for archiver, exec_list_by_archiver in get_executions_by_archiver(execution_infos).items():
        execution_times = []
        for artifact, exec_list_by_artifact in get_executions_by_artifact(exec_list_by_archiver).items():
            execution_times.extend([e.execution_time for e in exec_list_by_artifact])
        bar_chart.add(f"{archiver}", execution_times)

    bar_chart.x_labels = get_executions_by_artifact(execution_infos).keys()
    bar_chart.render_to_file(os.path.join(common_paths.render_path, f'{sys.platform}.svg'))
    a.embed(type="image/svg+xml", src=f'{sys.platform}.svg', style="height: calc(100vh - 5px);")


def get_executions_by_artifact(execution_infos):
    execution_by_artifact: dict[str, list[models.ExecutionInfo]] = {}
    for execution in execution_infos:
        if execution.artifact.name not in execution_by_artifact:
            execution_by_artifact[execution.artifact.name] = []

        execution_by_artifact[execution.artifact.name].append(execution)
    return execution_by_artifact


def get_executions_by_archiver(exec_list_by_artifact):
    execution_by_archiver: dict[str, list[models.ExecutionInfo]] = {}
    for execution in exec_list_by_artifact:
        if execution.archiver not in execution_by_archiver:
            execution_by_archiver[execution.archiver] = []

        execution_by_archiver[execution.archiver].append(execution)
    return execution_by_archiver
