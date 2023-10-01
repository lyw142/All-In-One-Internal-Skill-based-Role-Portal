<script>

import StaffNavigation from "./components/StaffNavigation.vue";
import createrolelisting from "./views/CreateRoleListing.vue"

export default {
  name: 'App',
  components: { StaffNavigation, createrolelisting },
  data() {
    return {
      title: 'SPM Sprint 1'
    }
  },
  computed: {
    show() {
      return 2
    }
  }
}
</script>

<template>
  <StaffNavigation v-if="show == 1" />
  <createrolelisting v-if="show == 2" />
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
