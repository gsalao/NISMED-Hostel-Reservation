<script setup>
import nismedLogo from '@/assets/images/nismed-logo.png'
</script>

<template>
  <nav class="fixed top-0 w-full z-30 bg-[#09240B]">
    <div class="max-w-screen-xl mx-auto px-4 py-3 flex justify-between items-center text-white">
      <span class="font-bold text-xl md:text-2xl flex items-center space-x-2">
        <img :src="nismedLogo" alt="UP NISMED Logo" class="h-10 w-auto">
        <span>UP NISMED Hostel</span>
      </span>
      <ul class="flex space-x-4 text-lg md:text-2xl">
        <li><a href="#" class="hover:underline">Home</a></li>
        <li><a href="#" class="hover:underline">About</a></li>
        <li><a href="#" class="hover:underline">Contact</a></li>
      </ul>
    </div>
  </nav>
</template>
