<template>
  <div>
    <h1>Register Yourself</h1>
    <input
      type="email"
      name="email"
      v-model="email"
      placeholder="Enter your email address"
    />
    <br />
    <input
      type="password"
      name="password"
      v-model="password"
      placeholder="Create a new password"
    />
    <br />
    <button @click="register">Register</button>
  </div>
</template>

<script>
import authentication_service from "@/services/authentication_service";
export default {
  data() {
    return {
      email: "",
      password: ""
    };
  },
  methods: {
    async register() {
      await authentication_service.register({
        email: this.email,
        password: this.password
      });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
