<script setup lang="ts">
import Footer from './components/Footer.vue'
import NavBar from './components/NavBar.vue'
</script>

<template>
  <!-- Full-page layout -->
  <div class="relative min-h-screen flex flex-col">

    <!-- Background image layer -->
    <div class="absolute inset-0 z-0">
      <!-- insert default background image here -->
      <!-- atm, this is set to a white background -->
    </div>

    <NavBar />

      <main class="flex-grow relative z-10">
        <router-view />
      </main>

    <!-- Footer always at bottom -->
    <Footer />
  </div>
</template>

<style>
  div {
    font-family: 'inter';
  }
</style>