<template>
  <nav class="fixed top-0 w-full z-30 bg-[#09240B]">
    <div class="max-w-screen-xl mx-auto px-4 py-3 flex justify-between items-center text-white">
      <span class="font-bold text-xl md:text-2xl flex items-center space-x-2">
        <img :src="nismedLogo" alt="UP NISMED Logo" class="h-10 w-auto">
        <span>UP NISMED Hostel</span>
      </span>
      <ul class="flex space-x-4 text-lg md:text-2xl">
        <li>
          <button @click="goToHome" class="cursor-pointer hover:underline">Home</button>
        </li>

        <li>
          <button @click="goToBookingForm" class="hover:underline">Book</button>
        </li>

        <li>
          <button @click="scrollToFooter" class="hover:underline">Contact</button>
        </li>

      </ul>
    </div>
  </nav>
</template>

<script setup lang="ts">
  import nismedLogo from '@/assets/images/nismed-logo.png'  
  import { useRoute, useRouter } from "vue-router";

  const route = useRoute();
  const router = useRouter();

  const goToHome = () => {
    if (route.path === "/") {
      // Already on the homepage, scroll to top smoothly
      window.scrollTo({ top: 0, behavior: "smooth" });
    } else {
      // Navigate to homepage
      router.push("/");
    }
  };

    const goToBookingForm = () => {
    if (route.path === "/booking-form/") {
      // Already on the homepage, scroll to top smoothly
      window.scrollTo({ top: 0, behavior: "smooth" });
    } else {
      // Navigate to homepage
      router.push("/booking-form/");
    }
  };

  const scrollToFooter = () => {
    const footerElement = document.getElementById("contact-section");
    if (footerElement) {
      footerElement.scrollIntoView({ behavior: "smooth" });
    } else {
      console.error("Footer element not found.");
    }
  };
</script>