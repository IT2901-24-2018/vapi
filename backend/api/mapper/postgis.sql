/*
This file contain useful sql commands for map matching
*/


-- Distance between point and linestring using geometry, returning distance in useless-units.
SELECT
ST_Distance(
  ST_GeomFromText('POINT(63.3870750023729 10.3277250005425)', 32633),
  ST_GeomFromText(
    'LINESTRING(266711 7037272,266712 7037276,266747 7037300,266793 7037316,266826 7037325,266835 7037327)',
    32633
  )
);


-- Linestring as extended wkt
SELECT ST_AsEWKT(
  ST_GeomFromText(
    'LINESTRING(266711 7037272,266712 7037276,266747 7037300,266793 7037316,266826 7037325,266835 7037327)',
    32633
  )
);


-- Linestring as text
SELECT ST_AsText(ST_GeogFromText('SRID=4326;LINESTRING(-72.1260 42.45, -72.123 42.1546)'));


-- Transform geometry from one srid to another
SELECT ST_Transform(
  ST_GeomFromText(
    'LINESTRING(266711 7037272,266712 7037276,266747 7037300,266793 7037316,266826 7037325,266835 7037327)',
    32633
  ),
  4326
);


-- Select the_geom as text form table
SELECT ST_AsText(the_geom) FROM api_dummymodel;


-- Segment with the shortest distance from point and under MAX_MAPPING_DISTANCE
-- Placeholders are lon, lat and MAX_MAPPING_DISTANCE.
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
