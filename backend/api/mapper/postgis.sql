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
  the_geom::geography,
  ST_GeogFromText('SRID=4326;POINT(-72.1260 42.45)')
)
FROM api_dummymodel;


SELECT ST_Transform(ST_GeomFromText('LINESTRING(266711 7037272,266712 7037276,266747 7037300,266793 7037316,266826 7037325,266835 7037327)', 32633), 4326);

'LINESTRING(10.3292530834357 63.3874948034588,10.3292671984426 63.387531236765,10.329930199592 63.387768783352,10.3308242225738 63.3879419520468,10.3314692019554 63.3880440103041,10.3316457680236 63.3880677779613)'


-- Select the_geom as text
SELECT ST_AsText(the_geom) FROM api_dummymodel;


-- Segment with the shortest distance from point and under MAX_MAPPING_DISTANCE
WITH segment (id, distance)
AS
-- Find distance to segment and id
(
  SELECT S.id AS id,
  ST_Distance(S.the_geom::geography,
  ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography) AS distance
  FROM api_dummymodel S
)
SELECT id, distance
FROM segment
WHERE distance <= %s
ORDER BY distance ASC
LIMIT 1
