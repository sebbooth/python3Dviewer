import numpy as np
## CREDIT:
# https://rosettacode.org/wiki/Find_the_intersection_of_a_line_with_a_plane#Python
	
def LinePlaneCollision(planeNormal, planePoint, rayDirection, rayPoint, epsilon=1e-6):

	ndotu = planeNormal.dot(rayDirection)
	if abs(ndotu) < epsilon:
		raise RuntimeError("no intersection or line is within plane")

	w = rayPoint - planePoint
	si = -planeNormal.dot(w) / ndotu
	Psi = w + si * rayDirection + planePoint
	return Psi



def normalize(v):
	norm = np.linalg.norm(v)
	if norm == 0:
		return v
	return v / norm
