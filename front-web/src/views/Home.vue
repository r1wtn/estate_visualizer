<template>
  <div id="container">
    <GlobalMap />
  </div>
</template>

<script>
// @ is an alias to /src
import GlobalMap from "@/components/GlobalMap.vue";

export default {
  name: "Home",
  components: {
    GlobalMap
  }
};
</script>

<style>
#container {
  margin-left: 60px;
  margin-right: 60px;
}
</style>
