<template>
  <section class="relative h-screen w-full text-white z-10">
    <!-- Background Image -->
    <div
      class="absolute inset-0 bg-cover bg-center z-0"
      :style="{ backgroundImage: `url(${nismedHero})` }"
    ></div>

    <!-- Overlay -->
    <div class="absolute inset-0 bg-black opacity-80 z-10"></div>

    
    <!-- Hero Content -->
    <div class="relative z-20 flex flex-col items-center justify-center text-center h-full px-4">
      <h1 class="text-5xl md:text-7xl font-bold text-yellow-500 drop-shadow-lg">UP NISMED Hostel</h1>
      <p class="mt-4 text-lg md:text-2xl text-yellow-400 font-sm drop-shadow-lg">
        The Hostel provides a quiet retreat for its guests, a second-home ambience, and a haven for the professional and transients.
        
        <!-- TODO: insert more info; uncomment following txt: -->
        <!-- The hostel has forty-eight (48) rooms and can accommodate a maximum of 120 guests. Each room is equipped with a telephone. Free Wi-Fi is also available. -->
      </p>
    </div>
  </section>
</template>

<script setup>
import nismedHero from '@/assets/images/nismed-hostel-landing.jpg'
</script>
