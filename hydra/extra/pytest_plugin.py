# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
from pathlib import Path
from typing import Callable, List, Optional

import pytest
from omegaconf.basecontainer import BaseContainer

from hydra.core.singleton import Singleton
from hydra.test_utils.test_utils import SweepTaskFunction, TaskTestFunction
from hydra.types import TaskFunction


@pytest.fixture(scope="function")  # type: ignore
def hydra_restore_singletons() -> None:
    """
    Restore singletons state after the function returns
    """
    state = copy.deepcopy(Singleton.get_state())
    resolvers = copy.deepcopy(BaseContainer._resolvers)
    yield
    Singleton.set_state(state)
    BaseContainer._resolvers = resolvers


@pytest.fixture(scope="function")  # type: ignore
def hydra_sweep_runner() -> Callable[
    [
        Optional[str],
        Optional[str],
        Optional[TaskFunction],
        Optional[str],
        Optional[str],
        Optional[List[str]],
        Optional[bool],
        Optional[Path],
    ],
    SweepTaskFunction,
]:
    def _(
        calling_file: Optional[str],
        calling_module: Optional[str],
        task_function: Optional[TaskFunction],
        config_path: Optional[str],
        config_name: Optional[str],
        overrides: Optional[List[str]],
        strict: Optional[bool] = None,
        temp_dir: Optional[Path] = None,
    ) -> SweepTaskFunction:
        sweep = SweepTaskFunction()
        sweep.calling_file = calling_file
        sweep.calling_module = calling_module
        sweep.task_function = task_function
        sweep.config_path = config_path
        sweep.config_name = config_name
        sweep.strict = strict
        sweep.overrides = overrides or []
        sweep.temp_dir = str(temp_dir)
        return sweep

    return _


@pytest.fixture(scope="function")  # type: ignore
def hydra_task_runner() -> Callable[
    [
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[List[str]],
        Optional[bool],
    ],
    TaskTestFunction,
]:
    def _(
        calling_file: Optional[str],
        calling_module: Optional[str],
        config_path: Optional[str],
        config_name: Optional[str],
        overrides: Optional[List[str]] = None,
        strict: Optional[bool] = None,
    ) -> TaskTestFunction:
        task = TaskTestFunction()
        task.overrides = overrides or []
        task.calling_file = calling_file
        task.config_name = config_name
        task.calling_module = calling_module
        task.config_path = config_path
        task.strict = strict
        return task

    return _
