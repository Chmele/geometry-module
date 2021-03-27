# Computational geometry algotrithms module
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/9630c9cb0ce44acdb3d2f4c15e27cde7)](https://www.codacy.com/gh/Chmele/geometry-module/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Chmele/geometry-module&amp;utm_campaign=Badge_Grade)

## Contents
This module contains implementations for computational geometry algorithms based upon Franco P. Preparata and Michael I. Shamos' book "Computational Geometry: An Introduction". These algorithms are subdivided in three topics: geometric searching, constructing convex hulls, and proximity problems.
#### Geometric searching
* Point location
    * *Slab method*: locate a point in a planar graph between its two edges.
    * *Chain method*: locate a point in a planar graph between its two monotone chains connecting its lower-most and upper-most vertices.
    * *Triangulation refinement method **(TBD)***: locate a point in a triangulated planar graph in one of the triangles.
    * *Trapezoid method **(TBD)***:  locate a point in a trapezoidal partition of a planar graph in one of its trapezoids.
* Range-searching
    * *k-D tree method*: find out which or how many points of a given set lie in a specified range, using a multidimensional binary tree (here, 2-*D* tree).
    * *Range-tree method **(TBD)**: find out which or how many points of a given set lie in a specified range, using a range tree data structure.
    * *Loci method*: find out how many points of a given set lie in a specified range, using a region (locus) partition of the searching space.
#### Constructing convex hulls
* Static problem
    * *Graham's scan*: construct the convex hull of a given set of points, using a stack of points.
    * *Quickhull*: construct the convex hull of a given set of points, using the partitioning of the set and merging the subsets similar to those in Quicksort algorithm.
    * *Divide-and-conquer*: given the convex hulls of the two subsets of a given set of points, merge them into a convex hull of the entire set of points.
    * *Jarvis' march*: construct the convex hull of a given set of points, using the so-called gift wrapping technique.
* Dynamic problem
    * *Preparata's algorithm **(TBD)***: construct the convex hull of a set of points being dynamically added to a current hull.
    * *Dynamic convex hull maintenance **(TBD)***: construct the convex hull of a set of points and re-construct it on addition or deletion of a point.
#### Proximity problems
* *Divide-and-conquer closest pair search **(TBD)***: given a set of points, find the two points with the smallest mutual distance, using divide-and-conquer approach.
* *Divide-and-conquer Voronoi diagram constructing **(TBD)***: given a set points, construct their Voronoi diagram, using divide-and-conquer approach.