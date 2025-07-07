<!-- Landing Page View -->
 
<template>
  <div>
    <HeroSlider />
    <div id="landing-page-bulk"class="flex flex-col md:flex-row gap-6 px-4 md:px-10">
      <!-- Left Section: Amenities, Rates, Hours -->
      <div class="flex-1 space-y-6">
        <AmenitiesLanding />
        <RatesLanding />
        <OperatingHours />
      </div>

      <!-- Right Section: Room Gallery -->
      <div class="flex-1 w-full space-y-12 self-center">
        <div class="w-full">
          <RoomGallery :images="roomSetA" />
        </div>
        <div class="w-full">
          <RoomGallery :images="roomSetB" />
        </div>
        <div class="w-full">
          <RoomGallery :images="roomSetC" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import HeroSlider from '../components/HeroSlider.vue'
  import RoomGallery from '../components/RoomGallery.vue'
  import RatesLanding from '../components/RatesLanding.vue'
  import AmenitiesLanding from '../components/AmenitiesLanding.vue'
  import OperatingHours from '../components/OperatingHours.vue'

  const images = import.meta.glob('@/assets/images/*.{png,jpg,jpeg,avif,webp}', { eager: true, import: 'default' })

  const roomSetA: Array<{ src: string, label: string }> = []
  const roomSetB: Array<{ src: string, label: string }> = []
  const roomSetC: Array<{ src: string, label: string }> = []

  Object.entries(images).forEach(([path, src]) => {
    if (path.includes('Type-A')) {
      roomSetA.push({ src: src as string, label: 'Room Type A' })
    } else if (path.includes('Type-B')) {
      roomSetB.push({ src: src as string, label: 'Room Type B' })
    } else if (path.includes('Type-C')) {
      roomSetC.push({ src: src as string, label: 'Room Type C' })
    }
  })

  roomSetA.sort((a, b) => a.src.localeCompare(b.src))
  roomSetB.sort((a, b) => a.src.localeCompare(b.src))
  roomSetC.sort((a, b) => a.src.localeCompare(b.src))
</script>