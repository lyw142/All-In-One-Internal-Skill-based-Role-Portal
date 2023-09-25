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
    <!-- form starts here -->
    <div class="container min-vh-100 d-flex justify-content-center align-items-center">
        <form class="border border-secondary-subtle rounded col-7" style="padding: 20px;">
            <div class="mb-2 border-bottom">
                <p style="font-weight: bold;">Role details</p>
            </div>
            <div class="mb-3">
                <label for="roletitle" class="form-label">Role title</label>
                <input type="text" class="form-control" id="roletitle">
            </div>
            <div class="mb-3">
                <label for="roledescription">Role description</label>
                <textarea class="form-control rounded" id="roledescription" rows="10"></textarea>
            </div>
            <div class="mb-3">
                <label for="skills">Add skills</label>
                <select class="form-select form-select-sm" aria-label="Small select example">
                    <option selected>Open this select menu</option>
                    <option value="1">One</option>
                    <option value="2">Two</option>
                    <option value="3">Three</option>
                </select>
            </div>

            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>
</template>
  
  
<script>

export default {
    name: "testform",
}
</script>
  
<style scoped>
.btn {
    margin: 10px;
}
</style>