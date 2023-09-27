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
            <a class="nav-link active" aria-current="page" href="#1">Role listings</a>
          </li>

        </ul>
        <button type="button" class="btn btn-secondary">Logout</button>
      </div>
    </div>
  </nav>
  <!-- search bar here -->
  <div class="row g-3 align-items-center" style="padding-top: 30px;padding-left: 50px;">
    <div class="col-auto">
      <label class="col-form-label">Search</label>
    </div>
    <!-- search box  -->
    <div class="col-auto">
      <input type="text" class="form-control">
    </div>
    <!-- dummy column  -->
    <div class="col-auto">
    </div>
  </div>
  <!-- body starts here -->
  <div class="container" style="padding-top: 50px;">
    <div class="row align-items-start">
      <!-- left role listing column -->
      <div class="col-5">
        <!-- card 1 -->
        <div class="card mb-3" v-for="job in joblistings">
          <div class="card-body">
            <div class="row">
              <h5 class="card-title">{{ job.Role_Name }}</h5>
            </div>
            <p class="card-text">Skills required:</p>
            <!-- skills container  -->
            <div class="container">
              <span class="badge text-bg-secondary">Secondary</span>
              <span class="badge text-bg-secondary">Secondary</span>
              <span class="badge text-bg-success">Success</span>
              <span class="badge text-bg-secondary">Secondary</span>
              <span class="badge text-bg-secondary">Secondary</span>
              <span class="badge text-bg-secondary">Secondary</span>
              <span class="badge text-bg-secondary">Secondary</span>
              <span class="badge text-bg-success">Success</span>
            </div>
            <p style="padding-top: 10px;">Application deadline: {{ job.Deadline }}</p>
          </div>
        </div>
        {{ joblistings }}
      </div>
      <div class="col-7">
        <div class="card" style="position: fixed;">
          <div class="card-body">
            <h5 class="card-title">Special title treatment</h5>
            <p class="card-text">With supporting text below as a natural lead-in to additional content. Lorem ipsum dolor
              sit amet consectetur adipisicing elit. Quibusdam ullam nam tenetur ducimus optio earum repellat aut quos
              nesciunt, soluta qui odio aperiam. Illum tempore eum corrupti accusamus a sapiente? Lorem ipsum dolor sit
              amet consectetur adipisicing elit. Reprehenderit explicabo, perferendis ut nisi molestias excepturi? Quia
              ipsum quos earum illum tenetur expedita impedit! Debitis quia nesciunt commodi dignissimos eaque beatae!
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Numquam libero necessitatibus sint impedit, ipsa
              itaque similique ratione molestiae! Rerum corporis, nobis itaque facilis vitae minima amet dicta! Vitae,
              suscipit non!</p>
            <a href="#" class="btn btn-primary">Go somewhere</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';


export default {
  data() {
    return {
      joblistings: []
    }
  },
  mounted() {
    axios.get('http://127.0.0.1:5000/joblistings').then(response => this.joblistings = response.data)
  },
  name: "StaffNavigation",
}
</script>

<style scoped>
.btn {
  margin: 10px;
}

p {
  font-size: smaller;
}

span {
  margin: 2px;
}

ul {
  font-size: smaller;
}
</style>