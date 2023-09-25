<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary" data-bs-theme="dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="#"><img src="../assets/logo.png" height="50" width="50"></a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="#1">Roles</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Candidates</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">View staff skills</a>
          </li>
        </ul>
        <button type="button" class="btn btn-secondary">Logout</button>
      </div>
    </div>
  </nav>
</template>


<script>

export default {
  name: "HRNavigation",
}
</script>

<style scoped>
.btn {
  margin: 10px;
}
</style>