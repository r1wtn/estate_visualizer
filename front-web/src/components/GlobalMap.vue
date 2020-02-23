<template>
  <div id="global-map"></div>
</template>

<script>
import { ACCESS_TOKEN } from "@/properties/mapbox";
import mapboxgl from "mapbox-gl";
import MapboxLanguage from "@mapbox/mapbox-gl-language";
import "mapbox-gl/dist/mapbox-gl.css";
import axios from "axios";

// 2050年の人口から10段階のカテゴリ別に分類するためのフィルタ
let PT0_2050_1 = ["<", ["get", "PT0_2050"], 4000];
let PT0_2050_2 = [
  "all",
  [">=", ["get", "PT0_2050"], 4000],
  ["<", ["get", "PT0_2050"], 8000]
];
let PT0_2050_3 = [
  "all",
  [">=", ["get", "PT0_2050"], 8000],
  ["<", ["get", "PT0_2050"], 12000]
];
let PT0_2050_4 = [
  "all",
  [">=", ["get", "PT0_2050"], 12000],
  ["<", ["get", "PT0_2050"], 16000]
];
let PT0_2050_5 = [
  "all",
  [">=", ["get", "PT0_2050"], 16000],
  ["<", ["get", "PT0_2050"], 20000]
];
let PT0_2050_6 = [
  "all",
  [">=", ["get", "PT0_2050"], 20000],
  ["<", ["get", "PT0_2050"], 24000]
];
let PT0_2050_7 = [
  "all",
  [">=", ["get", "PT0_2050"], 24000],
  ["<", ["get", "PT0_2050"], 28000]
];
let PT0_2050_8 = [
  "all",
  [">=", ["get", "PT0_2050"], 28000],
  ["<", ["get", "PT0_2050"], 32000]
];
let PT0_2050_9 = [
  "all",
  [">=", ["get", "PT0_2050"], 32000],
  ["<", ["get", "PT0_2050"], 36000]
];
let PT0_2050_10 = [
  "all",
  [">=", ["get", "PT0_2050"], 36000],
  ["<", ["get", "PT0_2050"], 40000]
];

// 色の設定
let colors = [
  "rgb(215, 25, 28)",
  "rgb(232, 91, 58)",
  "rgb(249, 158, 89)",
  "rgb(254, 201, 128)",
  "rgb(255, 237, 170)",
  "rgb(237, 247, 201)",
  "rgb(199, 230, 219)",
  "rgb(157, 207, 228)",
  "rgb(100, 165, 205)",
  "rgb(44, 123, 182)"
];

export default {
  name: "GlobalMap",
  props: {},

  data() {
    return {
      map: null,
      popup: new mapboxgl.Popup({
        closeButton: false,
        closeOnClick: false
      })
    };
  },

  mounted() {
    this.initLayer();
  },
  methods: {
    initLayer() {
      mapboxgl.accessToken = ACCESS_TOKEN;
      this.map = new mapboxgl.Map({
        container: "global-map",
        style: "mapbox://styles/mapbox/light-v9",
        center: [139.657125, 35.661236],
        zoom: 10,
        pitch: 40
      });
      this.map.addControl(new MapboxLanguage({ defaultLanguage: "ja" }));
      this.map.addControl(new mapboxgl.NavigationControl());
      let scale = new mapboxgl.ScaleControl({
        maxWidth: 250,
        unit: "metric"
      });
      this.map.addControl(scale);
      // mapがロードされた際の処理を定義
      this.map.on("load", this.mapOnLoaded);
      this.map.on("mousemove", "2DmeshLayer", this.mapOnMouseMove);
      this.map.on("mouseleave", "2DmeshLayer", this.mapOnMouseLeave);
    },
    mapOnLoaded() {
      let meshGeoJsonURL =
        "https://raw.githubusercontent.com/valuecreation/mapbox-prj/b014b62e2c4db92726ca35ca8ec9a52b2acd5f28/data/1km_mesh_2018_13.geojson";
      axios.get(meshGeoJsonURL).then(meshdata => {
        console.log(meshdata.data);
        this.meshToMap(meshdata.data);
      });
    },
    meshToMap(meshdata) {
      // map.addSource に 読み込んだ GeoJSON を設定
      this.map.addSource("meshdata", {
        type: "geojson",
        data: meshdata
      });
      // map.addLayer で メッシュの色や幅、塗り潰し等の見た目を設定して、メッシュを表示
      // メッシュの色分け表示は、case オプションにより人口の属性値で分けて表示するように設定
      this.map.addLayer({
        id: "2DmeshLayer",
        type: "fill",
        source: "meshdata",
        layout: {},
        paint: {
          "fill-color": [
            "case",
            PT0_2050_1,
            colors[0],
            PT0_2050_2,
            colors[1],
            PT0_2050_3,
            colors[2],
            PT0_2050_4,
            colors[3],
            PT0_2050_5,
            colors[4],
            PT0_2050_6,
            colors[5],
            PT0_2050_7,
            colors[6],
            PT0_2050_8,
            colors[7],
            PT0_2050_9,
            colors[8],
            PT0_2050_10,
            colors[9],
            colors[9]
          ],
          "fill-outline-color": "white",
          "fill-opacity": 0.4
        }
      });
    },
    // マウスポインタがメッシュの領域に入ったら属性情報をポップアップで表示
    mapOnMouseMove(e) {
      this.map.getCanvas().style.cursor = "pointer";
      this.popup
        .setLngLat(e.lngLat)
        .setHTML(
          "<div><b>市区町村コード &nbsp;</b>" +
            e.features[0].properties.SHICODE +
            "</div>" +
            "<div><b>坪単価 (2月24日12時現在)</b></div>" +
            "<div>" +
            Math.round(e.features[0].properties.PT0_2050) +
            " 円</div>"
        )
        .addTo(this.map);
    },
    // マウスポインタがメッシュの領域から離れたらポップアップをクリア
    mapOnMouseLeave() {
      this.map.getCanvas().style.cursor = "";
      this.popup.remove();
    }
  }
};
</script>
<style>
#global-map {
  position: relative;
  top: 0;
  bottom: 0;
  width: 100%;
  height: 600px;
}
</style>
