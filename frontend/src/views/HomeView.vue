<script setup lang="ts">
import HeroSlider from '../components/HeroSlider.vue'
import RoomGallery from '../components/RoomGallery.vue'
import RatesLanding from '../components/RatesLanding.vue'
import AmenitiesLanding from '../components/AmenitiesLanding.vue'
import OperatingHours from '../components/OperatingHours.vue'
import typeA1 from '@/assets/images/Type-A-1.jpg'
import typeA2 from '@/assets/images/Type-A-2.jpg'
import typeA3 from '@/assets/images/Type-A-3.jpg'
import typeB1 from '@/assets/images/Type-B-1.jpg'
import typeB2 from '@/assets/images/Type-B-2.jpg'
import typeB3 from '@/assets/images/Type-B-3.jpg'
import typeC1 from '@/assets/images/Type-C-1.jpg'
import typeC2 from '@/assets/images/Type-C-2.jpg'
import typeC3 from '@/assets/images/Type-C-3.jpg'

const roomSetA = [
  { src: typeA1, label: "Room Type A" },
  { src: typeA2, label: "Room Type A" },
  { src: typeA3, label: "Room Type A" },
];

const roomSetB= [
  { src: typeB1, label: "Room Type B" },
  { src: typeB2, label: "Room Type B" },
  { src: typeB3, label: "Room Type B" },
];

const roomSetC = [
  { src: typeA1, label: "Room Type C" },
  { src: typeA2, label: "Room Type C" },
  { src: typeA3, label: "Room Type C" },
];
</script>

<template>
  <div>
    <HeroSlider />
    <div class="flex flex-col md:flex-row gap-6 px-4 md:px-10">
      <!-- Left Section: Amenities, Rates, Hours -->
      <div class="flex-1 space-y-6">
        <AmenitiesLanding />
        <RatesLanding />
        <OperatingHours />
      </div>

      <!-- Right Section: Room Gallery -->
      <div class="flex-1 space-y-12 self-center  ">
        <RoomGallery :images="roomSetA" />
        <RoomGallery :images="roomSetB" />
        <RoomGallery :images="roomSetC" />
      </div>
    </div>
  </div>
</template>