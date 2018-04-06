-- Distance between point and linestring using geometry, returning distance in useless-units.
SELECT
ST_Distance(
  ST_GeomFromText('POINT(63.3870750023729 10.3277250005425)', 32633),
  ST_GeomFromText('LINESTRING(266711 7037272,266712 7037276,266747 7037300,266793 7037316,266826 7037325,266835 7037327)', 32633));


-- Linestring as extended wkt
SELECT ST_AsEWKT(ST_GeomFromText('LINESTRING(266711 7037272,266712 7037276,266747 7037300,266793 7037316,266826 7037325,266835 7037327)', 32633));


-- Linestring as text
SELECT ST_AsText(ST_GeogFromText('SRID=4326;LINESTRING(-72.1260 42.45, -72.123 42.1546)'));


-- Distance between point and linestring using geography, returning distance in meters.
-- Requires lon lat point/linestring.
SELECT
ST_Distance(
  ST_GeogFromText('SRID=4326;LINESTRING(-72.1260 42.45, -72.123 42.1546)'),
  ST_GeogFromText('SRID=4326;POINT(-72.1260 42.45)')
);
