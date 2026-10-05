# 🧮 Matrix Operations CLI App

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![NumPy](https://img.shields.io/badge/numpy-required-orange)
![License](https://img.shields.io/badge/license-MIT-green)

A feature-rich, command-line Python application for evaluating and manipulating mathematical matrices. Built with NumPy, this tool allows users to input matrices on the fly and perform everything from basic arithmetic to advanced linear algebra calculations.

## 📑 Table of Contents
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage & Input Formatting](#-usage--input-formatting)
- [Operations Guide](#-operations-guide)
- [Roadmap](#-roadmap)

## ✨ Features

The application is divided into two main mathematical categories:

### 1. Basic Operations
Perform element-wise or dot-product arithmetic between your primary matrix and:
* **Scalars:** Addition, subtraction, and scalar multiplication.
* **Vectors/Matrices:** Addition, subtraction, and matrix multiplication.

### 2. Advanced Operations
Evaluate matrix properties or generate derived matrices:
* **Determinant & Singularity:** Calculate the determinant and check if a matrix is singular (non-invertible).
* **Transpose:** Swap rows and columns.
* **Symmetry:** 
  * Check if a matrix is symmetric or skew-symmetric.
  * Convert a matrix into a symmetric matrix.
  * Randomly generate symmetric or skew-symmetric matrices of any size.
* **Inverse & Adjoint:** Compute the multiplicative inverse and adjoint matrices.
* **Cofactor Matrix:** Generate the matrix of cofactors.
* **Rank:** Determine the linear independence of the matrix rows/columns.

## 📋 Prerequisites

* **Python 3.10 or higher:** The script utilizes structural pattern matching (`match`/`case`), which was introduced in Python 3.10.
* **NumPy:** Used for core matrix calculations and linear algebra functions.

## 🚀 Installation

1. Clone the repository or download the script file.
2. Install the required dependency using pip:
   ```bash
   pip install numpy
