SELECT  DISTINCT ON (h.host) --,inventory.location_lat, inventory.location_lon )
        h.host as host_name,
        max(t.priority) AS max_severity,
        inventory.location_lat AS "lat", 
        inventory.location_lon AS "lon"
        
FROM    hosts AS h
        INNER JOIN items AS i
          ON ( i.hostid = h.hostid ) 
        INNER JOIN functions AS f
          ON ( f.itemid = i.itemid )
        INNER JOIN triggers AS t
          ON ( t.triggerid = f.triggerid ),
        host_inventory AS inventory
        
WHERE  inventory.hostid=h.hostid AND inventory.location_lon!='' AND t.value!=0

Group by h.host, inventory.location_lat, inventory.location_lon
ORDER BY h.host DESC--, inventory.location_lat, inventory.location_lon
