<template>
  <section class="relative h-[60vh] w-full text-white z-10 flex items-center justify-center">
    <!-- Background Image -->
    <div
      class="absolute inset-0 bg-cover bg-center z-0"
      :style="{ backgroundImage: `url(${nismedHero})` }"
    ></div>

    <!-- Overlay -->
    <div class="absolute inset-0 bg-black opacity-80 z-10"></div>

    <!-- Hero Content -->
    <div class="relative z-20 flex flex-col items-center justify-center text-center px-4">
      <h1 class="text-5xl md:text-7xl font-bold text-yellow-500 drop-shadow-lg">UP NISMED Hostel</h1>
      <p class="mt-4 text-lg md:text-2xl text-yellow-400 font-sm drop-shadow-lg">
        The Hostel provides a quiet retreat for its guests, a second-home ambience, and a haven for the professional and transients.
      </p>

      <!-- Book Now Button -->
      <router-link
        to="/booking-form/"
        class="cursor-pointer mt-12 px-8 py-4 bg-yellow-500 text-black font-bold text-2xl rounded-lg shadow-lg hover:bg-yellow-600 transition-all duration-300 flex items-center justify-center"
      >
        Book Now
      </router-link>
    </div>
  </section>
</template>

<script setup>
  import nismedHero from '@/assets/images/nismed-hostel-landing.jpg'
</script>
