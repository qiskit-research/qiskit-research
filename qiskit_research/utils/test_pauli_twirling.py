# This code is part of Qiskit.
#
# (C) Copyright IBM 2022.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Test Pauli twirling."""

import unittest

import numpy as np
from qiskit.circuit import Parameter, QuantumCircuit
from qiskit.quantum_info import Operator
from qiskit_research.utils.pauli_twirling import add_pauli_twirls


class TestPauliTwirling(unittest.TestCase):
    """Test Pauli twirling."""

    def test_add_pauli_twirls(self):
        rng = np.random.default_rng()

        theta = Parameter("$\\theta$")
        phi = Parameter("$\\phi")

        circuit = QuantumCircuit(3)
        circuit.h([1, 2])
        circuit.rzx(theta, 0, 1)
        circuit.h(1)
        circuit.rzx(phi, 1, 2)
        circuit.rzz(theta, 0, 1)
        circuit.h(1)
        circuit.rzz(phi, 1, 2)
        circuit.h(2)
        twirled_circs = add_pauli_twirls(circuit, num_twirled_circuits=5)
        more_twirled_circs = add_pauli_twirls(
            [circuit], num_twirled_circuits=5, seed=1234
        )

        param_bind = {param: rng.uniform(-10, 10) for param in circuit.parameters}
        circuit.assign_parameters(param_bind, inplace=True)

        for t_circ in twirled_circs:
            t_circ.assign_parameters(param_bind, inplace=True)
            self.assertNotEqual(t_circ, circuit)
            self.assertTrue(Operator(t_circ).equiv(Operator(circuit)))

        for t_circ in more_twirled_circs[0]:
            t_circ.assign_parameters(param_bind, inplace=True)
            self.assertNotEqual(t_circ, circuit)
            self.assertTrue(Operator(t_circ).equiv(Operator(circuit)))