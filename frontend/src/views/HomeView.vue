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
  import { ref, onMounted } from 'vue'

  interface RoomImage {
    id: number
    name: string
    image: string
    room_type: number
    label?: string
    src?: string
  }

  const roomSetA = ref<{ src: string; label: string }[]>([])
  const roomSetB = ref<{ src: string; label: string }[]>([])
  const roomSetC = ref<{ src: string; label: string }[]>([])

  const allImages = ref<RoomImage[]>([])

  onMounted(async () => {
    try {
      const backendUrl = import.meta.env.VITE_BACKEND_BASE_URL
      // const mediaUrl = import.meta.env.VITE_BACKEND_URL
      const res = await fetch(`${backendUrl}/room/get_all_room_type_images/`)

      const data: RoomImage[] = await res.json()

      allImages.value = data

      // If your RoomType IDs are: A=1, B=2, C=3 (adjust if needed)
      roomSetA.value = data
        .filter(img => img.room_type === 3)
        .map(img => ({
          src: `${img.image}`,
          label: 'Room Type A'
        }))

      roomSetB.value = data
        .filter(img => img.room_type === 2)
        .map(img => ({
          src: `${img.image}`,
          label: 'Room Type B'
        }))

      roomSetC.value = data
        .filter(img => img.room_type === 1)
        .map(img => ({
          src: `${img.image}`,
          label: 'Room Type C'
        }))
    } catch (err) {
      console.error('Failed to fetch room images:', err)
    }
  })
</script>
