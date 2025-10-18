"""Simple Rubik's Cube 3x3 model.

This module provides a minimal `Cube` class suitable for building a solver later.

Representation:
 - Faces stored as dict with keys: U, D, L, R, F, B
 - Each face is a 3x3 list of single-character color codes.

Supported moves: R, R', L, L', U, U', D, D', F, F', B, B'

This file intentionally keeps implementation simple and clear rather than optimized.
"""

from __future__ import annotations

from copy import deepcopy
from random import choice, randint, shuffle
from typing import Dict, List


class Cube:
	"""A minimal 3x3 Rubik's Cube model.

	Methods:
	- apply_move(move)
	- apply_moves(seq)
	- scramble(n)
	- is_solved()
	"""

	FACE_KEYS = ("U", "D", "L", "R", "F", "B")

	def __init__(self):
		# Use single-letter colors per face for simplicity
		colors = {"U": "W", "D": "Y", "L": "O", "R": "R", "F": "G", "B": "B"}
		self.faces: Dict[str, List[List[str]]] = {k: [[colors[k]] * 3 for _ in range(3)] for k in self.FACE_KEYS}

	def copy(self) -> "Cube":
		c = Cube()
		c.faces = deepcopy(self.faces)
		return c

	# --- Utilities ---
	def _rotate_face_cw(self, face: List[List[str]]) -> None:
		# Rotate a 3x3 face clockwise in-place
		# Transpose + reverse rows
		face[:] = [list(row) for row in zip(*face[::-1])]

	def _rotate_face_ccw(self, face: List[List[str]]) -> None:
		# Rotate counter-clockwise: 3x cw
		self._rotate_face_cw(face)
		self._rotate_face_cw(face)
		self._rotate_face_cw(face)

	def is_solved(self) -> bool:
		"""Return True if every face has uniform color."""
		for k in self.FACE_KEYS:
			face = self.faces[k]
			color = face[0][0]
			for r in face:
				if any(c != color for c in r):
					return False
		return True

	# --- Move application ---
	def apply_move(self, move: str) -> None:
		"""Apply a single move in standard notation, e.g. "R" or "R'"."""
		prime = move.endswith("'")
		m = move[0]
		if m not in self.FACE_KEYS:
			raise ValueError(f"Unknown move: {move}")

		# For each move we rotate the face and cycle the adjacent edge stickers.
		# We'll implement the 6 face moves explicitly for clarity.
		if m == 'U':
			self._move_U(prime)
		elif m == 'D':
			self._move_D(prime)
		elif m == 'L':
			self._move_L(prime)
		elif m == 'R':
			self._move_R(prime)
		elif m == 'F':
			self._move_F(prime)
		elif m == 'B':
			self._move_B(prime)

	def apply_moves(self, seq: str) -> None:
		"""Apply a sequence of moves separated by spaces or given as an iterable string like "R U R' U'"."""
		tokens = seq.split() if isinstance(seq, str) else list(seq)
		for t in tokens:
			if not t:
				continue
			self.apply_move(t)

	def scramble(self, n: int = 25) -> List[str]:
		"""Apply n random moves and return the scramble as a list of moves."""
		base = list(self.FACE_KEYS)
		modifiers = ["", "'"]
		scramble = []
		prev = None
		for _ in range(n):
			m = choice(base)
			# avoid immediate inverse on same face
			if prev and m == prev:
				# pick different face
				candidates = [x for x in base if x != prev]
				m = choice(candidates)
			mod = choice(modifiers)
			move = m + mod
			self.apply_move(move)
			scramble.append(move)
			prev = m
		return scramble

	# --- Individual face move implementations ---
	def _move_U(self, prime: bool):
		# Rotate U face
		if prime:
			self._rotate_face_ccw(self.faces['U'])
		else:
			self._rotate_face_cw(self.faces['U'])

		# Cycle top rows of F, R, B, L
		F = self.faces['F'][0].copy()
		R = self.faces['R'][0].copy()
		B = self.faces['B'][0].copy()
		L = self.faces['L'][0].copy()
		if prime:
			self.faces['F'][0] = R
			self.faces['R'][0] = B
			self.faces['B'][0] = L
			self.faces['L'][0] = F
		else:
			self.faces['F'][0] = L
			self.faces['R'][0] = F
			self.faces['B'][0] = R
			self.faces['L'][0] = B

	def _move_D(self, prime: bool):
		if prime:
			self._rotate_face_ccw(self.faces['D'])
		else:
			self._rotate_face_cw(self.faces['D'])

		# Cycle bottom rows of F, L, B, R (note orientation)
		F = self.faces['F'][2].copy()
		L = self.faces['L'][2].copy()
		B = self.faces['B'][2].copy()
		R = self.faces['R'][2].copy()
		if prime:
			self.faces['F'][2] = L
			self.faces['L'][2] = B
			self.faces['B'][2] = R
			self.faces['R'][2] = F
		else:
			self.faces['F'][2] = R
			self.faces['L'][2] = F
			self.faces['B'][2] = L
			self.faces['R'][2] = B

	def _move_L(self, prime: bool):
		if prime:
			self._rotate_face_ccw(self.faces['L'])
		else:
			self._rotate_face_cw(self.faces['L'])

		# Cycle left columns of U, F, D, B (careful with B orientation)
		Ucol = [self.faces['U'][r][0] for r in range(3)]
		Fcol = [self.faces['F'][r][0] for r in range(3)]
		Dcol = [self.faces['D'][r][0] for r in range(3)]
		Bcol = [self.faces['B'][2 - r][2] for r in range(3)]  # reversed
		if prime:
			# U <- F, F <- D, D <- B, B <- U
			for r in range(3):
				self.faces['U'][r][0] = Fcol[r]
				self.faces['F'][r][0] = Dcol[r]
				self.faces['D'][r][0] = Bcol[r]
				self.faces['B'][2 - r][2] = Ucol[r]
		else:
			for r in range(3):
				self.faces['U'][r][0] = Bcol[r]
				self.faces['F'][r][0] = Ucol[r]
				self.faces['D'][r][0] = Fcol[r]
				self.faces['B'][2 - r][2] = Dcol[r]

	def _move_R(self, prime: bool):
		if prime:
			self._rotate_face_ccw(self.faces['R'])
		else:
			self._rotate_face_cw(self.faces['R'])

		Ucol = [self.faces['U'][r][2] for r in range(3)]
		Fcol = [self.faces['F'][r][2] for r in range(3)]
		Dcol = [self.faces['D'][r][2] for r in range(3)]
		Bcol = [self.faces['B'][2 - r][0] for r in range(3)]
		if prime:
			for r in range(3):
				self.faces['U'][r][2] = Fcol[r]
				self.faces['F'][r][2] = Dcol[r]
				self.faces['D'][r][2] = Bcol[r]
				self.faces['B'][2 - r][0] = Ucol[r]
		else:
			for r in range(3):
				self.faces['U'][r][2] = Bcol[r]
				self.faces['F'][r][2] = Ucol[r]
				self.faces['D'][r][2] = Fcol[r]
				self.faces['B'][2 - r][0] = Dcol[r]

	def _move_F(self, prime: bool):
		if prime:
			self._rotate_face_ccw(self.faces['F'])
		else:
			self._rotate_face_cw(self.faces['F'])

		Urow = self.faces['U'][2].copy()
		Rcol = [self.faces['R'][r][0] for r in range(3)]
		Drow = self.faces['D'][0].copy()
		Lcol = [self.faces['L'][2 - r][2] for r in range(3)]
		if prime:
			# U bottom <- R col, R col <- D top, D top <- L col, L col <- U bottom
			for i in range(3):
				self.faces['U'][2][i] = Rcol[i]
				self.faces['R'][i][0] = Drow[i]
				self.faces['D'][0][i] = Lcol[i]
				self.faces['L'][2 - i][2] = Urow[i]
		else:
			for i in range(3):
				self.faces['U'][2][i] = Lcol[i]
				self.faces['R'][i][0] = Urow[i]
				self.faces['D'][0][i] = Rcol[i]
				self.faces['L'][2 - i][2] = Drow[i]

	def _move_B(self, prime: bool):
		if prime:
			self._rotate_face_ccw(self.faces['B'])
		else:
			self._rotate_face_cw(self.faces['B'])

		Urow = self.faces['U'][0].copy()
		Lcol = [self.faces['L'][2 - r][0] for r in range(3)]
		Drow = self.faces['D'][2].copy()
		Rcol = [self.faces['R'][r][2] for r in range(3)]
		if prime:
			for i in range(3):
				self.faces['U'][0][i] = Lcol[i]
				self.faces['L'][2 - i][0] = Drow[i]
				self.faces['D'][2][i] = Rcol[i]
				self.faces['R'][i][2] = Urow[i]
		else:
			for i in range(3):
				self.faces['U'][0][i] = Rcol[i]
				self.faces['L'][2 - i][0] = Urow[i]
				self.faces['D'][2][i] = Lcol[i]
				self.faces['R'][i][2] = Drow[i]

	# --- String/printing helpers ---
	def __str__(self) -> str:
		# Pretty-print in a compact form
		out = []
		for k in self.FACE_KEYS:
			out.append(f"{k}:\n")
			for r in self.faces[k]:
				out.append("".join(r) + "\n")
		return "".join(out)


if __name__ == '__main__':
	# Quick demo: create, scramble, and check solved status
	c = Cube()
	print('Solved?', c.is_solved())
	scramble = c.scramble(20)
	print('Scramble:', ' '.join(scramble))
	print('Solved after scramble?', c.is_solved())
	print(c)

