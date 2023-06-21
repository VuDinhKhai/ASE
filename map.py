# import folium

# m = folium.Map()
# m.save("footprint.html")

# import folium

# m = folium.Map(location=(49.25, -123.12), tiles="cartodb positron")
# m.save("footprint.html")
import gmplot
  
# from_geocode method return the
# latitude and longitude of given location .
gmap2 = gmplot.GoogleMapPlotter.from_geocode( "Dehradun, India" )
  
gmap2.draw("map12.html" )