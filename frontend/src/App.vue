<script>

import StaffNavigation from "./components/StaffNavigation.vue";
import HRNavigation from "./components/HRNavigation.vue";
import testform from "./views/testform.vue"

export default {
  name: 'App',
  components: { StaffNavigation, HRNavigation, testform },
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
  <HRNavigation v-if="show == 1" />
  <StaffNavigation v-if="show == 2" />
  <testform v-if="show == 3" />
</template>


