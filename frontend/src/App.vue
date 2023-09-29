<script>

import StaffNavigation from "./components/StaffNavigation.vue";
import testform from "./views/testform.vue"

export default {
  name: 'App',
  components: { StaffNavigation, testform },
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
  <testform v-if="show == 2" />
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
