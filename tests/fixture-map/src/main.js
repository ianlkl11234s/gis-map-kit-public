import maplibregl from 'maplibre-gl';

const API_KEY = 'demo-1234567890abcdef'; // 環境部 API key
const map = new maplibregl.Map({
  container: 'map',
  style: 'https://tiles.example.com/style.json',
  center: [121.5, 25.05], zoom: 10,
  attributionControl: false,
});

async function load() {
  const res = await fetch(`https://data.moenv.gov.tw/api/v2/aqx_p_432?api_key=${API_KEY}&limit=1000`);
  const json = await res.json();
  const features = json.records.map(r => ({
    type: 'Feature',
    geometry: { type: 'Point', coordinates: [Number(r.longitude), Number(r.latitude)] },
    properties: { name: r.sitename, aqi: Number(r.aqi) || 0, time: r.publishtime },
  }));
  map.addSource('aqi', { type: 'geojson', data: { type: 'FeatureCollection', features } });
  map.addLayer({ id: 'aqi', type: 'circle', source: 'aqi', paint: {
    'circle-radius': 6,
    'circle-color': ['interpolate', ['linear'], ['get', 'aqi'], 0, '#eeeeee', 50, '#00e400', 100, '#ffff00', 150, '#ff7e00', 200, '#ff0000'],
  }});
  document.getElementById('legend').innerHTML = '綠 良好 / 黃 普通 / 橘 敏感族群 / 紅 不健康';
}

map.on('load', load);
map.on('mouseenter', 'aqi', e => {
  new maplibregl.Popup().setLngLat(e.lngLat).setHTML(e.features[0].properties.name + ' AQI ' + e.features[0].properties.aqi).addTo(map);
});
setInterval(() => { map.getSource('aqi') && load(); }, 60000);
