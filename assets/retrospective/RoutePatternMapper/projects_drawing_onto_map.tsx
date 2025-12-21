import React, { useState, useEffect, useRef } from 'react';
import { MapPin, Navigation, Filter, Bike, Footprints, Car, Trees, Pencil, Undo, Trash2, Upload, Check, Search, Repeat, ArrowRight, Download, Share2 } from 'lucide-react';

const RoutePatternMapper = () => {
  const [userLocation, setUserLocation] = useState(null);
  const [locationError, setLocationError] = useState(null);
  const [mapLoaded, setMapLoaded] = useState(false);
  const [routeTypes, setRouteTypes] = useState({
    bike: true,
    walking: false,
    road: false,
    trail: false
  });
  const [showRouteFilter, setShowRouteFilter] = useState(false);
  const [drawingMode, setDrawingMode] = useState(false);
  const [patternComplete, setPatternComplete] = useState(false);
  const [routeSearching, setRouteSearching] = useState(false);
  const [matchedRoute, setMatchedRoute] = useState(null);
  const [routeType, setRouteType] = useState('loop'); // 'loop' or 'open'
  const [searchProgress, setSearchProgress] = useState(0);
  const [searchStatus, setSearchStatus] = useState('');
  const [notification, setNotification] = useState(null);
  const [showExportMenu, setShowExportMenu] = useState(false);
  const [lineThickness, setLineThickness] = useState(3);
  const [drawnPaths, setDrawnPaths] = useState([]);
  const [currentPath, setCurrentPath] = useState([]);
  const [isDrawing, setIsDrawing] = useState(false);
  const [uploadedImage, setUploadedImage] = useState(null);
  const mapRef = useRef(null);
  const leafletMapRef = useRef(null);
  const userMarkerRef = useRef(null);
  const canvasRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    // Load Leaflet CSS
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.css';
    document.head.appendChild(link);

    // Load Leaflet JS
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js';
    script.onload = () => setMapLoaded(true);
    document.body.appendChild(script);

    return () => {
      document.head.removeChild(link);
      document.body.removeChild(script);
    };
  }, []);

  useEffect(() => {
    if (mapLoaded && mapRef.current && !leafletMapRef.current) {
      // Initialize map
      const L = window.L;
      const map = L.map(mapRef.current).setView([51.505, -0.09], 13);

      // Add OpenStreetMap tiles
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
      }).addTo(map);

      leafletMapRef.current = map;

      // Get user location
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const { latitude, longitude } = position.coords;
            setUserLocation({ lat: latitude, lng: longitude });
            
            // Center map on user location
            map.setView([latitude, longitude], 15);

            // Add marker for user location
            const userIcon = L.divIcon({
              className: 'custom-user-marker',
              html: '<div style="background: #3b82f6; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>',
              iconSize: [20, 20],
              iconAnchor: [10, 10]
            });

            userMarkerRef.current = L.marker([latitude, longitude], { icon: userIcon }).addTo(map);
          },
          (error) => {
            setLocationError(error.message);
            // Set default location for demo purposes (London)
            const defaultLat = 51.505;
            const defaultLng = -0.09;
            setUserLocation({ lat: defaultLat, lng: defaultLng });
            map.setView([defaultLat, defaultLng], 15);
            
            const userIcon = L.divIcon({
              className: 'custom-user-marker',
              html: '<div style="background: #3b82f6; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>',
              iconSize: [20, 20],
              iconAnchor: [10, 10]
            });

            userMarkerRef.current = L.marker([defaultLat, defaultLng], { icon: userIcon }).addTo(map);
          },
          {
            timeout: 5000,
            maximumAge: 0
          }
        );
      } else {
        setLocationError('Geolocation is not supported by your browser');
        // Set default location
        const defaultLat = 51.505;
        const defaultLng = -0.09;
        setUserLocation({ lat: defaultLat, lng: defaultLng });
        map.setView([defaultLat, defaultLng], 15);
        
        const userIcon = L.divIcon({
          className: 'custom-user-marker',
          html: '<div style="background: #3b82f6; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>',
          iconSize: [20, 20],
          iconAnchor: [10, 10]
        });

        userMarkerRef.current = L.marker([defaultLat, defaultLng], { icon: userIcon }).addTo(map);
      }
    }
  }, [mapLoaded]);

  const recenterMap = () => {
    if (leafletMapRef.current && userLocation) {
      leafletMapRef.current.setView([userLocation.lat, userLocation.lng], 15);
    }
  };

  const toggleRouteType = (type) => {
    setRouteTypes(prev => ({
      ...prev,
      [type]: !prev[type]
    }));
  };

  const getActiveRouteTypes = () => {
    return Object.keys(routeTypes).filter(type => routeTypes[type]);
  };

  const startDrawing = (e) => {
    if (!drawingMode) return;
    setIsDrawing(true);
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    setCurrentPath([{ x, y }]);
  };

  const draw = (e) => {
    if (!isDrawing || !drawingMode) return;
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    setCurrentPath(prev => [...prev, { x, y }]);
  };

  const stopDrawing = () => {
    if (isDrawing && currentPath.length > 0) {
      setDrawnPaths(prev => [...prev, { path: currentPath, thickness: lineThickness }]);
      setCurrentPath([]);
    }
    setIsDrawing(false);
  };

  const undoLastPath = () => {
    setDrawnPaths(prev => prev.slice(0, -1));
  };

  const clearCanvas = () => {
    setDrawnPaths([]);
    setCurrentPath([]);
    setUploadedImage(null);
    setPatternComplete(false);
    setMatchedRoute(null);
  };

  // Simplify path to key points for shape matching
  const simplifyPath = (paths) => {
    if (paths.length === 0) return [];
    
    const allPoints = [];
    paths.forEach(({ path }) => {
      allPoints.push(...path);
    });
    
    if (allPoints.length < 3) return allPoints;
    
    // Douglas-Peucker algorithm to simplify path
    const simplified = [allPoints[0]];
    const epsilon = 10; // Tolerance
    
    const simplifyRecursive = (points, start, end) => {
      if (end - start <= 1) return;
      
      let maxDist = 0;
      let maxIndex = start;
      
      for (let i = start + 1; i < end; i++) {
        const dist = perpendicularDistance(points[i], points[start], points[end]);
        if (dist > maxDist) {
          maxDist = dist;
          maxIndex = i;
        }
      }
      
      if (maxDist > epsilon) {
        simplifyRecursive(points, start, maxIndex);
        simplified.push(points[maxIndex]);
        simplifyRecursive(points, maxIndex, end);
      }
    };
    
    simplifyRecursive(allPoints, 0, allPoints.length - 1);
    simplified.push(allPoints[allPoints.length - 1]);
    
    return simplified;
  };
  
  const perpendicularDistance = (point, lineStart, lineEnd) => {
    const dx = lineEnd.x - lineStart.x;
    const dy = lineEnd.y - lineStart.y;
    const mag = Math.sqrt(dx * dx + dy * dy);
    if (mag === 0) return Math.sqrt(Math.pow(point.x - lineStart.x, 2) + Math.pow(point.y - lineStart.y, 2));
    
    const u = ((point.x - lineStart.x) * dx + (point.y - lineStart.y) * dy) / (mag * mag);
    const clampedU = Math.max(0, Math.min(1, u));
    
    const closestX = lineStart.x + clampedU * dx;
    const closestY = lineStart.y + clampedU * dy;
    
    return Math.sqrt(Math.pow(point.x - closestX, 2) + Math.pow(point.y - closestY, 2));
  };

  const showNotification = (message, type = 'error') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 5000);
  };

  // Generate GPX file for GPS devices
  const exportAsGPX = () => {
    if (!matchedRoute || !matchedRoute.coordinates) return;
    
    const routeName = `Route-${new Date().toISOString().split('T')[0]}`;
    const gpxHeader = `<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="Route Pattern Mapper" xmlns="http://www.topografix.com/GPX/1/1">
  <metadata>
    <name>${routeName}</name>
    <desc>Generated route matching custom pattern - ${matchedRoute.type === 'loop' ? 'Closed Loop' : 'Open Path'}</desc>
    <time>${new Date().toISOString()}</time>
  </metadata>
  <trk>
    <name>${routeName}</name>
    <type>${matchedRoute.routeTypes?.join(', ') || 'mixed'}</type>
    <trkseg>`;
    
    const gpxPoints = matchedRoute.coordinates.map(coord => 
      `      <trkpt lat="${coord[0]}" lon="${coord[1]}">
        <ele>0</ele>
      </trkpt>`
    ).join('\n');
    
    const gpxFooter = `
    </trkseg>
  </trk>
</gpx>`;
    
    const gpxContent = gpxHeader + '\n' + gpxPoints + gpxFooter;
    downloadFile(gpxContent, `${routeName}.gpx`, 'application/gpx+xml');
    showNotification('GPX file downloaded successfully!', 'success');
    setShowExportMenu(false);
  };

  // Generate KML file for Google Maps/Earth
  const exportAsKML = () => {
    if (!matchedRoute || !matchedRoute.coordinates) return;
    
    const routeName = `Route-${new Date().toISOString().split('T')[0]}`;
    const kmlHeader = `<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>${routeName}</name>
    <description>Generated route matching custom pattern - ${matchedRoute.type === 'loop' ? 'Closed Loop' : 'Open Path'}</description>
    <Style id="routeStyle">
      <LineStyle>
        <color>ff0000ff</color>
        <width>4</width>
      </LineStyle>
    </Style>
    <Placemark>
      <name>${routeName}</name>
      <description>Distance: ${matchedRoute.distance} km | Type: ${matchedRoute.routeTypes?.join(', ') || 'mixed'}</description>
      <styleUrl>#routeStyle</styleUrl>
      <LineString>
        <coordinates>`;
    
    const kmlCoords = matchedRoute.coordinates.map(coord => 
      `${coord[1]},${coord[0]},0`
    ).join(' ');
    
    const kmlFooter = `
        </coordinates>
      </LineString>
    </Placemark>
  </Document>
</kml>`;
    
    const kmlContent = kmlHeader + kmlCoords + kmlFooter;
    downloadFile(kmlContent, `${routeName}.kml`, 'application/vnd.google-earth.kml+xml');
    showNotification('KML file downloaded successfully!', 'success');
    setShowExportMenu(false);
  };

  // Export as JSON for app-specific use
  const exportAsJSON = () => {
    if (!matchedRoute) return;
    
    const routeData = {
      name: `Route-${new Date().toISOString().split('T')[0]}`,
      type: matchedRoute.type,
      distance: matchedRoute.distance,
      routeTypes: matchedRoute.routeTypes || getActiveRouteTypes(),
      coordinates: matchedRoute.coordinates,
      createdAt: new Date().toISOString(),
      pattern: drawnPaths.length > 0 ? {
        paths: drawnPaths.map(p => ({ points: p.path, thickness: p.thickness }))
      } : null
    };
    
    const jsonContent = JSON.stringify(routeData, null, 2);
    downloadFile(jsonContent, `${routeData.name}.json`, 'application/json');
    showNotification('JSON file downloaded successfully!', 'success');
    setShowExportMenu(false);
  };

  // Helper function to download files
  const downloadFile = (content, filename, mimeType) => {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  // Share route (for mobile devices with Web Share API)
  const shareRoute = async () => {
    if (!matchedRoute) return;
    
    const routeText = `Check out my route!\nDistance: ${matchedRoute.distance} km\nType: ${matchedRoute.type === 'loop' ? 'Closed Loop' : 'Open Path'}\nGenerated with Route Pattern Mapper`;
    
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'My Route',
          text: routeText
        });
        showNotification('Route shared successfully!', 'success');
      } catch (error) {
        if (error.name !== 'AbortError') {
          showNotification('Failed to share route', 'error');
        }
      }
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(routeText).then(() => {
        showNotification('Route details copied to clipboard!', 'success');
      }).catch(() => {
        showNotification('Share not supported on this device', 'warning');
      });
    }
    setShowExportMenu(false);
  };

  // Generate mock route data for demonstration
  // In production Android app, this would query OSM via native API calls
  const generateMockRouteData = (patternPoints, routeTypes, needsLoop) => {
    // Simulate finding routes based on the pattern
    const mockWays = [];
    
    // Create a simplified route that follows the pattern approximately
    const routeCoords = patternPoints.map(point => [point.lat, point.lng]);
    
    // If loop is needed, close the path
    if (needsLoop && routeCoords.length > 0) {
      routeCoords.push(routeCoords[0]);
    }
    
    // Calculate distance
    let distance = 0;
    for (let i = 1; i < routeCoords.length; i++) {
      distance += haversineDistance(
        { lat: routeCoords[i-1][0], lng: routeCoords[i-1][1] },
        { lat: routeCoords[i][0], lng: routeCoords[i][1] }
      );
    }
    
    return {
      coordinates: routeCoords,
      distance: distance.toFixed(2),
      type: needsLoop ? 'loop' : 'open',
      routeTypes: routeTypes
    };
  };

  const findMatchingRoute = async () => {
    setRouteSearching(true);
    setSearchProgress(0);
    setSearchStatus('Analyzing pattern...');
    
    try {
      // Simplify the drawn pattern
      setSearchProgress(10);
      const simplifiedPattern = simplifyPath(drawnPaths);
      
      if (simplifiedPattern.length < 2) {
        showNotification('Pattern too simple. Please draw a more detailed pattern.', 'error');
        setRouteSearching(false);
        return;
      }
      
      setSearchStatus('Getting map location...');
      setSearchProgress(20);
      
      // Get map bounds
      const bounds = leafletMapRef.current.getBounds();
      const centerLat = userLocation.lat;
      const centerLng = userLocation.lng;
      
      // Convert pattern points to lat/lng coordinates relative to map
      const canvasRect = canvasRef.current.getBoundingClientRect();
      const mapBounds = leafletMapRef.current.getBounds();
      
      setSearchStatus('Converting pattern to coordinates...');
      setSearchProgress(30);
      
      // Get the map container size
      const mapSize = leafletMapRef.current.getSize();
      
      const patternGeoPoints = simplifiedPattern.map(point => {
        // Calculate position relative to canvas center
        const relX = (point.x / canvasRect.width) - 0.5;
        const relY = (point.y / canvasRect.height) - 0.5;
        
        // Convert to lat/lng offset from center
        const latSpan = mapBounds.getNorth() - mapBounds.getSouth();
        const lngSpan = mapBounds.getEast() - mapBounds.getWest();
        
        return {
          lat: centerLat - (relY * latSpan),
          lng: centerLng + (relX * lngSpan)
        };
      });
      
      setSearchStatus('Building route query...');
      setSearchProgress(40);
      
      // Build route type filter
      const activeTypes = getActiveRouteTypes();
      
      if (activeTypes.length === 0) {
        showNotification('Please select at least one route type in the filter.', 'error');
        setRouteSearching(false);
        return;
      }
      
      setSearchStatus('Finding matching routes...');
      setSearchProgress(60);
      
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      setSearchStatus('Processing route data...');
      setSearchProgress(80);
      
      // DEMO MODE: Generate mock route based on pattern
      // NOTE: In production Android app, this would be replaced with actual
      // OSM API calls made through the app's native code or backend server
      const matchResult = generateMockRouteData(patternGeoPoints, activeTypes, routeType === 'loop');
      
      console.log('Demo route generated:', matchResult);
      
      console.log('Setting matched route...');
      setMatchedRoute(matchResult);
      console.log('Matched route state should be updated');
      
      setSearchStatus('Drawing route on map...');
      setSearchProgress(95);
      
      console.log('Match result:', matchResult);
      
      console.log('Match found!', matchResult);
      setMatchedRoute(matchResult);
      
      // Draw matched route on map
      if (matchResult.coordinates) {
        const L = window.L;
        const routeLine = L.polyline(matchResult.coordinates, {
          color: '#ef4444',
          weight: 5,
          opacity: 0.8
        }).addTo(leafletMapRef.current);
        
        // Store reference to remove later if needed
        matchResult.leafletLayer = routeLine;
        
        // Fit map to show the route
        leafletMapRef.current.fitBounds(routeLine.getBounds(), { padding: [50, 50] });
      }
      
      setSearchProgress(100);
      setSearchStatus('Complete!');
      
      setTimeout(() => {
        setSearchProgress(0);
        setSearchStatus('');
      }, 2000);
      
    } catch (error) {
      console.error('Route matching error:', error);
      showNotification('Error finding route: ' + error.message, 'error');
      setSearchProgress(0);
      setSearchStatus('');
    }
    
    setRouteSearching(false);
  };
  
  // Note: These functions are kept for reference but not used in demo mode
  // In production Android app, implement these server-side or via native API
  const matchPatternToRoutes = (patternPoints, ways, needsLoop) => {
    // This is a simplified matching algorithm
    // In production, this would use more sophisticated graph algorithms
    
    // Calculate pattern characteristics
    const patternLength = calculatePathLength(patternPoints);
    const patternBounds = getBounds(patternPoints);
    const patternCenter = {
      lat: (patternBounds.minLat + patternBounds.maxLat) / 2,
      lng: (patternBounds.minLng + patternBounds.maxLng) / 2
    };
    
    // Find ways that are within the pattern area
    const relevantWays = ways.filter(way => {
      if (!way.geometry || way.geometry.length < 2) return false;
      
      // Check if way intersects pattern bounding box
      const wayBounds = getBounds(way.geometry);
      return boundsIntersect(patternBounds, wayBounds);
    });
    
    if (relevantWays.length === 0) return null;
    
    // Try to build a route that matches the pattern
    let bestRoute = null;
    let bestScore = Infinity;
    
    // Simple greedy approach: connect ways that best match pattern direction
    for (let startWay of relevantWays) {
      const route = buildRoute(startWay, relevantWays, patternPoints, needsLoop);
      if (route) {
        const score = calculateShapeError(route.coordinates, patternPoints);
        if (score < bestScore) {
          bestScore = score;
          bestRoute = route;
        }
      }
    }
    
    // If score is too high (poor match), return null
    if (bestScore > patternLength * 0.5) return null;
    
    return bestRoute;
  };
  
  const buildRoute = (startWay, allWays, patternPoints, needsLoop) => {
    const route = [...startWay.geometry];
    const usedWays = new Set([startWay.id]);
    const maxSegments = 20;
    let segments = 1;
    
    while (segments < maxSegments) {
      const lastPoint = route[route.length - 1];
      
      // Find next connected way that best matches pattern direction
      let bestNext = null;
      let bestDist = Infinity;
      
      for (let way of allWays) {
        if (usedWays.has(way.id)) continue;
        if (!way.geometry || way.geometry.length < 2) continue;
        
        const firstPoint = way.geometry[0];
        const lastWayPoint = way.geometry[way.geometry.length - 1];
        
        const distToFirst = haversineDistance(lastPoint, firstPoint);
        const distToLast = haversineDistance(lastPoint, lastWayPoint);
        
        const minDist = Math.min(distToFirst, distToLast);
        
        if (minDist < 0.05 && minDist < bestDist) { // 50m threshold
          bestDist = minDist;
          bestNext = {
            way,
            reversed: distToLast < distToFirst
          };
        }
      }
      
      if (!bestNext) break;
      
      const nextGeom = bestNext.reversed 
        ? [...bestNext.way.geometry].reverse() 
        : bestNext.way.geometry;
      
      route.push(...nextGeom.slice(1));
      usedWays.add(bestNext.way.id);
      segments++;
    }
    
    // Check if loop closes
    if (needsLoop) {
      const dist = haversineDistance(route[0], route[route.length - 1]);
      if (dist > 0.1) return null; // Doesn't close within 100m
    }
    
    const distance = calculatePathLength(route);
    
    return {
      coordinates: route.map(p => [p.lat, p.lng]),
      distance: distance.toFixed(2),
      type: needsLoop ? 'loop' : 'open'
    };
  };
  
  const calculatePathLength = (points) => {
    let length = 0;
    for (let i = 1; i < points.length; i++) {
      length += haversineDistance(points[i - 1], points[i]);
    }
    return length;
  };
  
  const haversineDistance = (p1, p2) => {
    const R = 6371; // Earth radius in km
    const dLat = (p2.lat - p1.lat) * Math.PI / 180;
    const dLng = (p2.lng - p1.lng) * Math.PI / 180;
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(p1.lat * Math.PI / 180) * Math.cos(p2.lat * Math.PI / 180) *
              Math.sin(dLng / 2) * Math.sin(dLng / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  };
  
  const getBounds = (points) => {
    const lats = points.map(p => p.lat);
    const lngs = points.map(p => p.lng);
    return {
      minLat: Math.min(...lats),
      maxLat: Math.max(...lats),
      minLng: Math.min(...lngs),
      maxLng: Math.max(...lngs)
    };
  };
  
  const boundsIntersect = (b1, b2) => {
    return !(b1.maxLat < b2.minLat || b1.minLat > b2.maxLat ||
             b1.maxLng < b2.minLng || b1.minLng > b2.maxLng);
  };
  
  const calculateShapeError = (routeCoords, patternPoints) => {
    // Simple shape comparison: sum of distances from route points to nearest pattern points
    let error = 0;
    const sampleInterval = Math.max(1, Math.floor(routeCoords.length / 20));
    
    for (let i = 0; i < routeCoords.length; i += sampleInterval) {
      const routePoint = { lat: routeCoords[i][0], lng: routeCoords[i][1] };
      let minDist = Infinity;
      
      for (let patternPoint of patternPoints) {
        const dist = haversineDistance(routePoint, patternPoint);
        if (dist < minDist) minDist = dist;
      }
      
      error += minDist;
    }
    
    return error;
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setUploadedImage(event.target.result);
        setDrawnPaths([]);
        setCurrentPath([]);
      };
      reader.readAsDataURL(file);
    }
  };

  const finishPattern = () => {
    // Pattern is complete, ready for step 4
    setDrawingMode(false);
    setPatternComplete(true);
  };

  useEffect(() => {
    if ((drawingMode || patternComplete) && canvasRef.current) {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;

      // Clear canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Draw uploaded image if exists
      if (uploadedImage) {
        const img = new Image();
        img.onload = () => {
          ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        };
        img.src = uploadedImage;
      }

      // Draw all saved paths
      drawnPaths.forEach(({ path, thickness }) => {
        if (path.length < 2) return;
        ctx.beginPath();
        ctx.strokeStyle = '#3b82f6';
        ctx.lineWidth = thickness;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        ctx.moveTo(path[0].x, path[0].y);
        for (let i = 1; i < path.length; i++) {
          ctx.lineTo(path[i].x, path[i].y);
        }
        ctx.stroke();
      });

      // Draw current path being drawn
      if (currentPath.length > 1) {
        ctx.beginPath();
        ctx.strokeStyle = '#3b82f6';
        ctx.lineWidth = lineThickness;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        ctx.moveTo(currentPath[0].x, currentPath[0].y);
        for (let i = 1; i < currentPath.length; i++) {
          ctx.lineTo(currentPath[i].x, currentPath[i].y);
        }
        ctx.stroke();
      }
    }
  }, [drawingMode, patternComplete, drawnPaths, currentPath, lineThickness, uploadedImage]);

  return (
    <div className="w-full h-screen flex flex-col bg-gray-100">
      {/* Header */}
      <div className="bg-blue-600 text-white p-4 shadow-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <MapPin className="w-6 h-6" />
            <h1 className="text-xl font-bold">Route Pattern Mapper</h1>
          </div>
          <div className="text-sm">Step 1/4</div>
        </div>
      </div>

      {/* Map Container */}
      <div className="flex-1 relative">
        <div ref={mapRef} className="w-full h-full" />

        {/* Notification Toast */}
        {notification && (
          <div className={`absolute top-4 left-1/2 transform -translate-x-1/2 px-6 py-3 rounded-lg shadow-xl max-w-md text-center ${
            notification.type === 'error' ? 'bg-red-500 text-white' :
            notification.type === 'warning' ? 'bg-yellow-500 text-white' :
            'bg-green-500 text-white'
          }`} style={{ zIndex: 2000 }}>
            <p className="font-medium">{notification.message}</p>
          </div>
        )}

        {/* Drawing Canvas Overlay */}
        {(drawingMode || patternComplete) && (
          <canvas
            ref={canvasRef}
            className={`absolute inset-0 w-full h-full ${drawingMode ? 'cursor-crosshair' : 'pointer-events-none'}`}
            style={{ zIndex: 900 }}
            onMouseDown={drawingMode ? startDrawing : undefined}
            onMouseMove={drawingMode ? draw : undefined}
            onMouseUp={drawingMode ? stopDrawing : undefined}
            onMouseLeave={drawingMode ? stopDrawing : undefined}
            onTouchStart={drawingMode ? (e) => {
              e.preventDefault();
              const touch = e.touches[0];
              startDrawing({ clientX: touch.clientX, clientY: touch.clientY });
            } : undefined}
            onTouchMove={drawingMode ? (e) => {
              e.preventDefault();
              const touch = e.touches[0];
              draw({ clientX: touch.clientX, clientY: touch.clientY });
            } : undefined}
            onTouchEnd={drawingMode ? stopDrawing : undefined}
          />
        )}

        {/* Drawing Controls */}
        {drawingMode && (
          <div className="absolute top-4 left-4 bg-white rounded-lg shadow-xl p-4" style={{ zIndex: 1001 }}>
            <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
              <Pencil className="w-5 h-5 text-blue-600" />
              Draw Pattern
            </h3>
            
            <div className="space-y-3">
              {/* Thickness Control */}
              <div>
                <label className="text-sm text-gray-600 mb-1 block">
                  Line Thickness: {lineThickness}px
                </label>
                <input
                  type="range"
                  min="1"
                  max="10"
                  value={lineThickness}
                  onChange={(e) => setLineThickness(Number(e.target.value))}
                  className="w-full"
                />
              </div>

              {/* Action Buttons */}
              <div className="flex gap-2">
                <button
                  onClick={undoLastPath}
                  disabled={drawnPaths.length === 0}
                  className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
                >
                  <Undo className="w-4 h-4" />
                  Undo
                </button>
                <button
                  onClick={clearCanvas}
                  disabled={drawnPaths.length === 0 && !uploadedImage}
                  className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
                >
                  <Trash2 className="w-4 h-4" />
                  Clear
                </button>
              </div>

              {/* Upload Alternative */}
              <button
                onClick={() => fileInputRef.current?.click()}
                className="w-full flex items-center justify-center gap-2 px-3 py-2 bg-purple-100 text-purple-700 rounded-lg hover:bg-purple-200 text-sm font-medium"
              >
                <Upload className="w-4 h-4" />
                Upload Image Instead
              </button>
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                className="hidden"
              />

              {/* Done Button */}
              <button
                onClick={finishPattern}
                disabled={drawnPaths.length === 0 && !uploadedImage}
                className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
              >
                <Check className="w-5 h-5" />
                Done
              </button>

              <button
                onClick={() => setDrawingMode(false)}
                className="w-full px-3 py-2 text-sm text-gray-600 hover:text-gray-800"
              >
                Cancel
              </button>
            </div>
          </div>
        )}
        
        {/* Route Filter Button */}
        {userLocation && !drawingMode && (
          <button
            onClick={() => setShowRouteFilter(!showRouteFilter)}
            className="absolute top-4 right-4 bg-white p-3 rounded-lg shadow-lg hover:bg-gray-50 active:bg-gray-100 transition-colors flex items-center gap-2"
            style={{ zIndex: 1000 }}
          >
            <Filter className="w-5 h-5 text-blue-600" />
            <span className="text-sm font-medium text-gray-700">Routes</span>
            {getActiveRouteTypes().length > 0 && (
              <span className="bg-blue-600 text-white text-xs px-2 py-0.5 rounded-full">
                {getActiveRouteTypes().length}
              </span>
            )}
          </button>
        )}

        {/* Draw Pattern Button */}
        {userLocation && !drawingMode && !patternComplete && (
          <button
            onClick={() => setDrawingMode(true)}
            className="absolute top-20 right-4 bg-blue-600 text-white p-3 rounded-lg shadow-lg hover:bg-blue-700 active:bg-blue-800 transition-colors flex items-center gap-2"
            style={{ zIndex: 1000 }}
          >
            <Pencil className="w-5 h-5" />
            <span className="text-sm font-medium">Draw Pattern</span>
          </button>
        )}

        {/* Edit Pattern Button (after pattern is complete) */}
        {userLocation && !drawingMode && patternComplete && !matchedRoute && (
          <>
            <button
              onClick={() => setDrawingMode(true)}
              className="absolute top-20 right-4 bg-orange-600 text-white p-3 rounded-lg shadow-lg hover:bg-orange-700 active:bg-orange-800 transition-colors flex items-center gap-2"
              style={{ zIndex: 1000 }}
            >
              <Pencil className="w-5 h-5" />
              <span className="text-sm font-medium">Edit Pattern</span>
            </button>

            {/* Route Type Toggle and Find Route */}
            <div className="absolute top-40 right-4 bg-white rounded-lg shadow-xl p-4 w-64" style={{ zIndex: 1000 }}>
              <h3 className="font-semibold text-gray-800 mb-3">Find Route</h3>
              
              {/* Route Type Toggle */}
              <div className="flex gap-2 mb-4">
                <button
                  type="button"
                  onClick={() => {
                    console.log('Loop clicked');
                    setRouteType('loop');
                  }}
                  className={`flex-1 flex items-center justify-center gap-2 px-3 py-2 rounded-lg transition-colors ${
                    routeType === 'loop'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  <Repeat className="w-4 h-4" />
                  <span className="text-sm font-medium">Loop</span>
                </button>
                <button
                  type="button"
                  onClick={() => {
                    console.log('Open clicked');
                    setRouteType('open');
                  }}
                  className={`flex-1 flex items-center justify-center gap-2 px-3 py-2 rounded-lg transition-colors ${
                    routeType === 'open'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  <ArrowRight className="w-4 h-4" />
                  <span className="text-sm font-medium">Open</span>
                </button>
              </div>

              {/* Find Route Button */}
              <button
                type="button"
                onClick={() => {
                  console.log('Find Route clicked!', { routeSearching, drawnPaths: drawnPaths.length });
                  if (!routeSearching) {
                    findMatchingRoute();
                  }
                }}
                disabled={routeSearching}
                className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 active:bg-green-800 disabled:opacity-50 disabled:cursor-not-allowed font-semibold cursor-pointer"
              >
                {routeSearching ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    Searching...
                  </>
                ) : (
                  <>
                    <Search className="w-5 h-5" />
                    Find Route
                  </>
                )}
              </button>

              {/* Progress Bar */}
              {routeSearching && (
                <div className="mt-3">
                  <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                    <div 
                      className="bg-green-600 h-full transition-all duration-300"
                      style={{ width: `${searchProgress}%` }}
                    ></div>
                  </div>
                  <p className="text-xs text-gray-600 mt-2 text-center">{searchStatus}</p>
                </div>
              )}

              <p className="text-xs text-gray-500 mt-3">
                Very strict shape matching • No distance limit
              </p>
              
              <div className="mt-3 p-2 bg-blue-50 rounded text-xs text-blue-700">
                <strong>Demo Mode:</strong> Showing simulated routes. Production app will use native OSM API.
              </div>
            </div>
          </>
        )}

        {/* Route Type Filter Panel */}
        {showRouteFilter && userLocation && !drawingMode && (
          <div className="absolute top-20 right-4 bg-white rounded-lg shadow-xl w-64 p-4" style={{ zIndex: 1000 }}>
            <h3 className="font-semibold text-gray-800 mb-3">Route Types</h3>
            
            <div className="space-y-2">
              <button
                onClick={() => toggleRouteType('bike')}
                className={`w-full flex items-center gap-3 p-3 rounded-lg transition-colors ${
                  routeTypes.bike 
                    ? 'bg-blue-100 border-2 border-blue-600' 
                    : 'bg-gray-50 border-2 border-transparent hover:bg-gray-100'
                }`}
              >
                <Bike className={`w-5 h-5 ${routeTypes.bike ? 'text-blue-600' : 'text-gray-600'}`} />
                <span className={`font-medium ${routeTypes.bike ? 'text-blue-900' : 'text-gray-700'}`}>
                  Bike Paths
                </span>
                {routeTypes.bike && (
                  <div className="ml-auto w-5 h-5 bg-blue-600 rounded-full flex items-center justify-center">
                    <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                )}
              </button>

              <button
                onClick={() => toggleRouteType('walking')}
                className={`w-full flex items-center gap-3 p-3 rounded-lg transition-colors ${
                  routeTypes.walking 
                    ? 'bg-green-100 border-2 border-green-600' 
                    : 'bg-gray-50 border-2 border-transparent hover:bg-gray-100'
                }`}
              >
                <Footprints className={`w-5 h-5 ${routeTypes.walking ? 'text-green-600' : 'text-gray-600'}`} />
                <span className={`font-medium ${routeTypes.walking ? 'text-green-900' : 'text-gray-700'}`}>
                  Walking Paths
                </span>
                {routeTypes.walking && (
                  <div className="ml-auto w-5 h-5 bg-green-600 rounded-full flex items-center justify-center">
                    <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                )}
              </button>

              <button
                onClick={() => toggleRouteType('road')}
                className={`w-full flex items-center gap-3 p-3 rounded-lg transition-colors ${
                  routeTypes.road 
                    ? 'bg-orange-100 border-2 border-orange-600' 
                    : 'bg-gray-50 border-2 border-transparent hover:bg-gray-100'
                }`}
              >
                <Car className={`w-5 h-5 ${routeTypes.road ? 'text-orange-600' : 'text-gray-600'}`} />
                <span className={`font-medium ${routeTypes.road ? 'text-orange-900' : 'text-gray-700'}`}>
                  Roads
                </span>
                {routeTypes.road && (
                  <div className="ml-auto w-5 h-5 bg-orange-600 rounded-full flex items-center justify-center">
                    <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                )}
              </button>

              <button
                onClick={() => toggleRouteType('trail')}
                className={`w-full flex items-center gap-3 p-3 rounded-lg transition-colors ${
                  routeTypes.trail 
                    ? 'bg-emerald-100 border-2 border-emerald-600' 
                    : 'bg-gray-50 border-2 border-transparent hover:bg-gray-100'
                }`}
              >
                <Trees className={`w-5 h-5 ${routeTypes.trail ? 'text-emerald-600' : 'text-gray-600'}`} />
                <span className={`font-medium ${routeTypes.trail ? 'text-emerald-900' : 'text-gray-700'}`}>
                  Trails
                </span>
                {routeTypes.trail && (
                  <div className="ml-auto w-5 h-5 bg-emerald-600 rounded-full flex items-center justify-center">
                    <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                )}
              </button>
            </div>

            <div className="mt-4 pt-3 border-t border-gray-200">
              <p className="text-xs text-gray-500">
                Selected route types will be used for pattern matching
              </p>
            </div>
          </div>
        )}
        {/* Matched Route Info */}
        {matchedRoute && (
          <div className="absolute bottom-24 left-4 right-4 bg-white rounded-lg shadow-xl p-4" style={{ zIndex: 1000 }}>
            <div className="flex items-start justify-between mb-3">
              <div>
                <h3 className="font-bold text-lg text-gray-800">Route Found!</h3>
                <p className="text-sm text-gray-600">
                  {matchedRoute.type === 'loop' ? 'Closed Loop' : 'Open Path'}
                </p>
              </div>
              <button
                onClick={() => {
                  if (matchedRoute.leafletLayer) {
                    leafletMapRef.current.removeLayer(matchedRoute.leafletLayer);
                  }
                  setMatchedRoute(null);
                  setPatternComplete(false);
                  setShowExportMenu(false);
                }}
                className="text-gray-400 hover:text-gray-600"
              >
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-between py-2 border-t border-gray-200">
                <span className="text-sm text-gray-600">Distance</span>
                <span className="font-semibold text-gray-800">{matchedRoute.distance} km</span>
              </div>
              <div className="flex items-center justify-between py-2 border-t border-gray-200">
                <span className="text-sm text-gray-600">Route Types</span>
                <span className="font-semibold text-gray-800">{getActiveRouteTypes().join(', ')}</span>
              </div>
            </div>

            {/* Export Options */}
            <div className="mt-4 space-y-2">
              <button
                onClick={() => setShowExportMenu(!showExportMenu)}
                className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
              >
                <Download className="w-4 h-4" />
                Export & Save
              </button>

              {showExportMenu && (
                <div className="bg-gray-50 rounded-lg p-3 space-y-2">
                  <button
                    onClick={exportAsGPX}
                    className="w-full flex items-center gap-2 px-3 py-2 bg-white text-gray-700 rounded hover:bg-gray-100 text-sm font-medium"
                  >
                    <Download className="w-4 h-4" />
                    Download as GPX
                    <span className="text-xs text-gray-500 ml-auto">(Strava, Garmin)</span>
                  </button>
                  
                  <button
                    onClick={exportAsKML}
                    className="w-full flex items-center gap-2 px-3 py-2 bg-white text-gray-700 rounded hover:bg-gray-100 text-sm font-medium"
                  >
                    <Download className="w-4 h-4" />
                    Download as KML
                    <span className="text-xs text-gray-500 ml-auto">(Google Maps)</span>
                  </button>
                  
                  <button
                    onClick={exportAsJSON}
                    className="w-full flex items-center gap-2 px-3 py-2 bg-white text-gray-700 rounded hover:bg-gray-100 text-sm font-medium"
                  >
                    <Download className="w-4 h-4" />
                    Download as JSON
                    <span className="text-xs text-gray-500 ml-auto">(App data)</span>
                  </button>
                  
                  <button
                    onClick={shareRoute}
                    className="w-full flex items-center justify-center gap-2 px-3 py-2 bg-green-600 text-white rounded hover:bg-green-700 text-sm font-medium"
                  >
                    <Share2 className="w-4 h-4" />
                    Share Route
                  </button>
                </div>
              )}
            </div>

            <div className="mt-4 p-3 bg-green-50 rounded-lg">
              <p className="text-sm text-green-800">
                ✓ Route displayed in red on the map
              </p>
              <p className="text-xs text-gray-500 mt-2">
                Demo Mode: In production, routes will come from OpenStreetMap API via native backend
              </p>
            </div>
          </div>
        )}
        
        {/* Recenter Button */}
        {userLocation && !drawingMode && (
          <button
            onClick={recenterMap}
            className="absolute bottom-6 right-6 bg-white p-3 rounded-full shadow-lg hover:bg-gray-50 active:bg-gray-100 transition-colors"
            style={{ zIndex: 1000 }}
            aria-label="Recenter map"
          >
            <Navigation className="w-6 h-6 text-blue-600" />
          </button>
        )}

        {/* Location Error Message */}
        {locationError && userLocation && (
          <div className="absolute top-4 left-4 right-20 bg-yellow-500 text-white p-3 rounded-lg shadow-lg" style={{ zIndex: 1000 }}>
            <p className="font-semibold text-sm">Using demo location</p>
            <p className="text-xs mt-1">Location access unavailable - showing default location for testing</p>
          </div>
        )}

        {/* Loading Indicator */}
        {!userLocation && !locationError && (
          <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-75 z-[1000]">
            <div className="text-center">
              <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
              <p className="text-gray-700 font-medium">Finding your location...</p>
            </div>
          </div>
        )}
      </div>

      {/* Status Bar */}
      <div className="bg-white border-t border-gray-200 p-3">
        {userLocation ? (
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">
              Location: {userLocation.lat.toFixed(5)}, {userLocation.lng.toFixed(5)}
            </span>
            <span className="text-green-600 font-medium flex items-center gap-1">
              <div className="w-2 h-2 bg-green-600 rounded-full"></div>
              Connected
            </span>
          </div>
        ) : (
          <div className="text-center text-gray-500 text-sm">
            Waiting for location...
          </div>
        )}
      </div>
    </div>
  );
};

export default RoutePatternMapper;