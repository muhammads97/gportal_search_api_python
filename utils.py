def inside_polygon(px, py, x, y):
  counter = 0
  p1x = px[0]
  p1y = py[0]
  n = len(px)
  i = 1
  while (i<n):
    p2x = px[i % n]
    p2y = py[i % n]
    if (y > min(p1y,p2y)):
      if (y <= max(p1y,p2y)):
        if (x <= max(p1x,p2x)):
          if (p1y != p2y):
            xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
            if (p1x == p2x or x <= xinters):
              counter+=1
    p1x = p2x
    p1y = p2y
    i+=1

  if (counter % 2 == 0):
    return 0
  else:
    return 1
