import os.path

import pygal

from ArchiverCommon import artifact_tools, models, common_paths


def render(execution_infos: list[models.ExecutionInfo]) -> None:
    bar_chart = pygal.Bar()
    bar_chart.title = os.environ['self_toolset_name']

    for archiver, exec_list_by_archiver in get_executions_by_archiver(execution_infos).items():
        execution_times = []
        for artifact, exec_list_by_artifact in get_executions_by_artifact(exec_list_by_archiver).items():
            execution_times.extend([e.execution_time for e in exec_list_by_artifact])
        bar_chart.add(f"{archiver}", execution_times)

    bar_chart.x_labels = get_executions_by_artifact(execution_infos).keys()

    os.makedirs(common_paths.render_path, exist_ok=True)
    bar_chart.render_to_file(os.path.join(common_paths.render_path, f"{os.environ['self_toolset_name']}.svg"))


def get_executions_by_artifact(execution_infos):
    execution_by_artifact: dict[str, list[models.ExecutionInfo]] = {}
    for execution in execution_infos:
        if execution.artifact.name not in execution_by_artifact:
            execution_by_artifact[artifact_tools.get_pretty_name(execution.artifact)] = []

        execution_by_artifact[artifact_tools.get_pretty_name(execution.artifact)].append(execution)
    return execution_by_artifact


def get_executions_by_archiver(exec_list_by_artifact):
    execution_by_archiver: dict[str, list[models.ExecutionInfo]] = {}
    for execution in exec_list_by_artifact:
        if execution.archiver not in execution_by_archiver:
            execution_by_archiver[execution.archiver] = []

        execution_by_archiver[execution.archiver].append(execution)
    return execution_by_archiver
