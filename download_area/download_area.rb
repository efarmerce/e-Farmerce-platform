# Example code for Cumbum Region	

require 'rgeo'
require 'rgeo/geo_json'
require 'json'
require 'typhoeus'
require 'dotenv'
require 'uri'
require 'fileutils'

Dotenv.load

# Adjust for different zoom levels
DEFAULT_ZOOM = 19
lngOffset = 0.000696 #Calculated for latitude 9.688075284366109
latOffset = 0.000686

dir = "#{File.dirname(__FILE__)}/results" # Directory to save a csv file with all the lat lon points to download tiles for
BOTTOM_CROP = 23
IMAGE_SIZE = 256
CONCURRENT_DOWNLOADS = 100
SLEEP_BETWEEN_DOWNLOADS = 0

FileUtils.mkdir_p(dir)

$hydra = Typhoeus::Hydra.new


# Adjust this geojson section to represent the bounding box for area to download
str = <<GEOJSON
    {
      "type": "Feature",
      "properties": {
        "Name": "Cumbum"
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              77.28160858154297,
              9.718616881312279
            ],
            [
              77.27186679840088,
              9.722127717403033
            ],
            [
              77.25658893585204,
              9.703346430815616
            ],
            [
              77.28302478790283,
              9.699116265988055
            ],
            [
              77.28160858154297,
              9.718616881312279
            ]
          ]
        ]
      }
    }
GEOJSON


## This finds the bounding box of the geojson.  
p0 = JSON.parse(str)["geometry"]["coordinates"].first.first
maxLat, maxLng = p0
minLat, minLng = p0
JSON.parse(str)["geometry"]["coordinates"].first.each do |lat,lng|
  maxLat = lat if lat > maxLat
  print "maxLat ", maxLat, "  "
  minLat = lat if lat < minLat
  print "minLat ", minLat, "  "
  maxLng = lng if lng > maxLng
  print "maxLng ", maxLng, "  "
  minLng = lng if lng < minLng
  print "minLng ", minLng, "  "
  print "\n\n"
end


# This is the silly Java-ish initialization for the geography engine
factory = ::RGeo::Geos.factory

# This parses the geoJSON and turns it into a gemoetry object
feature = RGeo::GeoJSON.decode(str, json_parser: :json)
county_boundary = feature.geometry

saved_points = []

path = "#{dir}/points.csv"

if File.exist? path
  File.foreach(path) do |line|
    currentLat, currentLng = line.split(",")
    next if currentLat == "lat"
    saved_points.push({lat: currentLat.to_f, lng: currentLng.to_f})
  end
else
  # This opens the file and puts in a header 
  f = File.open(path, "w")
  f.puts "lat,lng"

  # This iterates through the points and adds a lat/lng pair
  # to the CSV for each point
  currentLat = minLat
  while currentLat <= maxLat
    currentLng = minLng
    while currentLng <= maxLng
      point = factory.point(currentLat,currentLng)
      if point.within?(county_boundary)
        f.puts "#{currentLng.round(7)},#{currentLat.round(7)}"
        saved_points.push({lng: currentLat.round(7), lat: currentLng.round(7)})
      end
      currentLng += lngOffset/2
    end
    currentLat += latOffset/2
  end

  # Clean up after yourself, says your mother.
  f.close
end
#--- 
def build_url(lat,lng,zoom=DEFAULT_ZOOM, size=IMAGE_SIZE)
  raise("No URL Defined")
end

lookup = {}
label = JSON.parse(str)["properties"]["NAME"]

# THis breaks them into batches
saved_points.each_slice(CONCURRENT_DOWNLOADS) do |slices|
#saved_points[0..20].each_slice(CONCURRENT_DOWNLOADS) do |slices|
  requests = []
  slices.each do |item|
    lat = item[:lat]
    lng = item[:lng]
    url = build_url(lat,lng, DEFAULT_ZOOM)
    filename = "#{label}_#{lat}_#{lng}_z#{DEFAULT_ZOOM}.png"
    lookup[url] = filename
    unless File.exist? "#{dir}/#{filename}"
      request = Typhoeus::Request.new(url, {followlocation: true, timeout: 300})
      $hydra.queue(request)
      requests.push request
    else
      #puts "skipping #{filename}"
    end
  end

  ## DOWNLOAD THE MAP TILES
  $hydra.run

  ## SAVE THEM TO DISK
  responses = requests.map { |r|
    puts "#{r.url}: #{r.response.status_message}"
    if r.response.status_message == 'OK' &&  r.response.body.size > 5000
      File.open("#{dir}/#{lookup[r.url]}","wb") do |f|
        f.puts r.response.response_body
      end
    end
  }
  unless requests.empty?
    sleep(SLEEP_BETWEEN_DOWNLOADS)
  end
end

lookup.values.each do |filename|
  path = "#{dir}/#{filename}"
  if File.exist? path
    sizes = IO.read(path)[0x10..0x18].unpack('NN') # hack for getting sizes from the bytes of a PNG
    unless sizes[0] == IMAGE_SIZE && sizes[1] == IMAGE_SIZE
      `mogrify -gravity north -extent  #{IMAGE_SIZE}x#{IMAGE_SIZE} #{path}`
    end
  end
end
