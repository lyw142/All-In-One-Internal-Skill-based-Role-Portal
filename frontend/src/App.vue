<script>

import StaffNavigation from "./components/StaffNavigation.vue";
import createrolelisting from "./views/CreateRoleListing.vue"
import HRNavigation from "./components/HRNavigation.vue"
export default {
  name: 'App',
  components: { StaffNavigation, createrolelisting, HRNavigation },
  data() {
    return {
      title: 'SPM Sprint 1'
    }
  },
  computed: {
    show() {
      return 3
    }
  }
}
</script>

<template>
  <StaffNavigation v-if="show == 1" />
  <createrolelisting v-if="show == 2" />
  <HRNavigation v-if="show == 3" />
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
