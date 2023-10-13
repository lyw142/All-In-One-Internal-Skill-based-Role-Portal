<script>

export default {
  name: 'App',
  data() {
    return {
      title: 'SPM Sprint 1'
    }
  },
}
</script>

<template>
  <router-link to="/staffnav">I am a staff member</router-link>
  <router-link to="/hrnav">I am from HR</router-link>
  <router-link to="/">go back home</router-link>

  <router-view></router-view>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
