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

  import { computed, onMounted } from 'vue'
  import { useHomePageStore } from '../stores/homePageStore'

  const store = useHomePageStore()

  const roomSetA = computed(() =>
    store.images.filter(img => img.room_type === 3).map(img => ({
      src: img.image,
      label: 'Room Type A'
    }))
  )

  const roomSetB = computed(() =>
    store.images.filter(img => img.room_type === 2).map(img => ({
      src: img.image,
      label: 'Room Type B'
    }))
  )

  const roomSetC = computed(() =>
    store.images.filter(img => img.room_type === 1).map(img => ({
      src: img.image,
      label: 'Room Type C'
    }))
  )

  onMounted(() => {
    store.loadAll()
  })
</script>
