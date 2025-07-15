from __future__ import annotations

import os
from functools import cached_property
from typing import TYPE_CHECKING, Self

import numpy as np
from numpy.random import default_rng
from pydantic import (
    BaseModel,
    ConfigDict,
    computed_field,
    field_validator,
    model_validator,
)
import base64
import io
import zlib
import hashlib

from qiskit.quantum_info import Statevector
from qiskit.primitives.containers.estimator_pub import EstimatorPub
from qiskit_ibm_runtime.options import NoiseLearnerOptions, TwirlingOptions

UNSUPPORTED_GATES = [
    "reset",
    "if_else",
    "for_loop",
    "switch_case",
    "measure",
]

class TEMOptions(BaseModel):
    tem_max_bond_dimension: int = (500,)
    compute_shadows_bias_from_observable: bool = False
    shadows_bias: np.ndarray = np.array([1 / 3, 1 / 3, 1 / 3])
    max_execution_time: int | None = None
    num_randomizations: int = 32
    max_layers_to_learn: int = 4
    default_precision: float = 0.02
    shots_per_randomization: int = 128
    layer_pair_depths: list[int] = [0, 1, 2, 4, 16, 32]

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    @field_validator("tem_max_bond_dimension")
    @classmethod
    def bd_must_be_less_than_equal_max_bond_dimension(cls, v: int) -> int:
        if v > 1000:
            raise ValueError(
                f"Unsupported option: Max bond dimension too large. tem_max_bond_dimension must be <= {1000:d}."
            )
        return v

    @field_validator("max_execution_time")
    @classmethod
    def max_execution_time_must_be_greater_than_60_seconds(
        cls, v: int | None
    ) -> int | None:
        if v is not None and v < 60:
            raise ValueError(
                f"Unsupported option: max_execution_time must be greater or equal than {60:d} seconds."
            )
        return v

    @field_validator("shadows_bias")
    @classmethod
    def validate_shadows_bias(cls, v: list | tuple | np.ndarray) -> np.ndarray:
        v = np.array(v)
        shape = v.shape
        if len(shape) > 2 and (shape[-1] != 3):
            raise ValueError(
                "Unsupported option: Mitigation_bias must be a 1d array of size 3 or a 2d one of shape (num_qubits, 3)."
            )
        if not np.allclose(v.sum(axis=-1), 1, atol=1e-5):
            raise ValueError(
                "Unsupported option: Not a valid probability distribution: the sum of the bias values must be 1."
            )
        if np.any(v < 0.1):
            raise ValueError(
                "Unsupported option: All the bias values must be >= 0.1. for QPU real implementations."
            )
        return v

    @model_validator(mode="after")
    def validate_shadows_bias_from_observable(self) -> Self:
        if self.compute_shadows_bias_from_observable and not np.allclose(
            self.shadows_bias, np.array([1 / 3, 1 / 3, 1 / 3]), atol=1e-8
        ):
            raise ValueError(
                "Unsupported option: When compute_shadows_bias_from_observable is True, "
                "you cannot also pass a custom-bias"
            )
        return self

    @computed_field(return_type=NoiseLearnerOptions)
    @property
    def noise_learner_options(self) -> NoiseLearnerOptions:
        return NoiseLearnerOptions(
            num_randomizations=self.num_randomizations,
            max_layers_to_learn=self.max_layers_to_learn,
            shots_per_randomization=self.shots_per_randomization,
            layer_pair_depths=self.layer_pair_depths,
            twirling_strategy="active-accum",
            environment={"job_tags": [32, "noise_learning"]},
        )

    @computed_field(return_type=TwirlingOptions)
    @property
    def twirling_options(self) -> TwirlingOptions:
        return TwirlingOptions(
            enable_gates=True,
            enable_measure=False,
            num_randomizations=1,
            shots_per_randomization="auto",
            strategy="active-accum",
        )


class TEMInputs:
    def __init__(
        self,
        arguments: dict,
    ) -> None:
        pubs: list[EstimatorPub] = arguments["pubs"]
        self.ibm_instance: str | None = arguments.get("instance")
        self.options: TEMOptions = TEMOptions(**arguments.get("options", {}))
        if not isinstance(pubs, list):
            pubs = [pubs]
        self.pubs = [EstimatorPub.coerce(pub) for pub in pubs]
        self.rng = default_rng(32)
        for pub in self.pubs:
            self.validate(pub)

    def validate(self, pub: EstimatorPub) -> None:
        if pub.parameter_values.num_parameters > 0:
            raise ValueError(
                "Unsupported circuit: parametrized circuits are not supported."
            )
        gate_types = pub.circuit.count_ops()
        for gate in UNSUPPORTED_GATES:
            if gate in gate_types:
                raise ValueError(f"Unsupported circuit: gate {gate} is not supported.")

def validation(
    arguments: dict,
) -> None:
    try:
        _t = TEMInputs(arguments)
        print("TEM input checks out")
    except Exception as e:
        print("TEM input validation failed:", e)
        raise e


def check_circuit(circuit):
    with io.BytesIO() as buff:
        np.save(buff, np.round(Statevector(circuit).probabilities(),7), allow_pickle=False)
        buff.seek(0)
        serialized_data = buff.read()
    serialized_data = zlib.compress(serialized_data)
    series = base64.standard_b64encode(serialized_data).decode("utf-8")
    hashed_circ = hashlib.sha256(series.encode("utf-8")).hexdigest()
    try:
        assert hashed_circ == "67b19a21308681a6d3d76e91eb4086773e0d861150f14a186ea30bd12c3aacff"
        print("Circuit verification successful! The quantum state matches the expected reference.")
    except AssertionError:
        print(f"Circuit verification failed! Got hash: {hashed_circ}")
        raise
