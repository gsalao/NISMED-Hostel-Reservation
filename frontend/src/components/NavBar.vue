<!-- NavBar View -->

<script setup lang="ts">
  import nismedHostelLogo from '@/assets/images/hostel-logo.jpg'  
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

<template>
  <nav class="fixed top-0 w-full z-30 bg-[#09240B]">
    <div class="max-w-screen-xl mx-auto px-4 py-3 flex justify-between items-center text-white">
      <button @click="goToHome" class="cursor-pointer font-bold text-xl md:text-2xl flex items-center space-x-2">
        <img :src="nismedHostelLogo" alt="UP NISMED Logo" class="h-10 w-auto">
        <span>UP NISMED Hostel</span>
      </button>
      <ul class="flex space-x-4 text-lg md:text-2xl">
        <li>
          <button @click="goToHome" class="cursor-pointer hover:underline">Home</button>
        </li>

        <li>
          <button @click="goToBookingForm" class="cursor-pointer hover:underline">Book</button>
        </li>

        <li>
          <button @click="scrollToFooter" class="cursor-pointer hover:underline">Contact</button>
        </li>

      </ul>
    </div>
  </nav>
</template>
