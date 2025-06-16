<script setup lang="ts">
import Footer from './components/Footer.vue'
import HeroSlider from './components/HeroSlider.vue'
import NavBar from './components/NavBar.vue'
import RoomGallery from './components/RoomGallery.vue'
</script>

<template>
  <!-- Full-page layout -->
  <div class="relative min-h-screen flex flex-col">

    <!-- Background image layer -->
    <div class="absolute inset-0 z-0">
      <!-- your background image goes here -->
    </div>

    <HeroSlider />
    <!-- Content (with relative context) -->
    <main class="relative z-10 flex-grow">
      <router-view />
    </main>

    <RoomGallery />

    <NavBar />

    <!-- Footer always at bottom -->
    <Footer />
  </div>
</template>

<style>
  div {
    font-family: 'inter';
  }
</style>