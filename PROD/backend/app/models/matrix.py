# app/models/matrix.py
from pydantic import BaseModel
from typing import List


class MatrixInput(BaseModel):
    matrix_A: List[List[float]]
    vector_b1: List[float]
    vector_b2: List[float]


class EigenvalueOutput(BaseModel):
    eigenvalues: List[float]


class DeterminantOutput(BaseModel):
    determinant: float
    uniqness: str


class ConditionNumberOutput(BaseModel):
    matrix_condition: float | str
    hilbert_condition: float


class PolynomialOutput(BaseModel):
    coefficients: List[float]


class PowerMethodOutput(BaseModel):
    largest_eigenvalue_A: float
    largest_eigenvalue_inverse_A: float
    lu_eigenvalues: List[float]


class SolutionOutput(BaseModel):
    solution: List[float]


class AllOperationsOutput(BaseModel):
    eigenvalues: List[float]
    determinant: float
    is_unique: bool
    condition_number: float
    hilbert_condition: float
    polynomial_coefficients: List[float]
    largest_eigenvalue_A: float
    largest_eigenvalue_inverse_A: float
    solution_b1: List[float]
    solution_b2: List[float]
